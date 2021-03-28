"""
Train model using FinRL
"""

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = str(parent.parent.parent).replace("\\", "\\\\")
import sys
sys.path.insert(0, srcPath)

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use('Agg')
import datetime

from finrl.config import config
from finrl.marketdata.yahoodownloader import YahooDownloader
from finrl.preprocessing.preprocessors import FeatureEngineer
from finrl.preprocessing.data import data_split
from finrl.env.env_stocktrading import StockTradingEnv
from finrl.env.env_portfolio import StockPortfolioEnv

from finrl.model.models import DRLAgent,DRLEnsembleAgent
from finrl.trade.backtest import backtest_stats, get_baseline, backtest_plot

from pprint import pprint

import sys
sys.path.append("../FinRL-Library")

import itertools

import os
if not os.path.exists("./" + config.DATA_SAVE_DIR):
    os.makedirs("./" + config.DATA_SAVE_DIR)
if not os.path.exists("./" + config.TRAINED_MODEL_DIR):
    os.makedirs("./" + config.TRAINED_MODEL_DIR)
if not os.path.exists("./" + config.TENSORBOARD_LOG_DIR):
    os.makedirs("./" + config.TENSORBOARD_LOG_DIR)
if not os.path.exists("./" + config.RESULTS_DIR):
    os.makedirs("./" + config.RESULTS_DIR)
    
from ohlc import preprocess as prep

if __name__ == "__main__":
    
    # TODO : integrate with our own preprocessor
    # TODO : df = prep.preprocess(size=500, symbols=['AAPL'], to_csv=True)
    
    df = YahooDownloader(start_date = config.START_DATE,
                        end_date = config.END_COLLECT_DATE,
                        ticker_list = config.NAS_100_TICKER).fetch_data()

    df.sort_values(['date','tic']).head()
    
    fe = FeatureEngineer(
                    use_technical_indicator=True,
                    tech_indicator_list = config.TECHNICAL_INDICATORS_LIST,
                    use_turbulence=True,
                    user_defined_feature = False)

    processed = fe.preprocess_data(df)

    list_ticker = processed["tic"].unique().tolist()
    list_date = list(pd.date_range(processed['date'].min(),processed['date'].max()).astype(str))
    combination = list(itertools.product(list_date,list_ticker))

    processed_full = pd.DataFrame(combination,columns=["date","tic"]).merge(processed,on=["date","tic"],how="left")
    processed_full = processed_full[processed_full['date'].isin(processed['date'])]
    processed_full = processed_full.sort_values(['date','tic'])

    processed_full = processed_full.fillna(0)
    
    stock_dimension = len(processed_full.tic.unique())
    state_space = 1 + 2*stock_dimension + len(config.TECHNICAL_INDICATORS_LIST)*stock_dimension
    print(f"Stock Dimension: {stock_dimension}, State Space: {state_space}")
    
    env_kwargs = {
        "hmax": 100, 
        "initial_amount": 50_000_000/100, #Since in Indonesia the minimum number of shares per trx is 100, then we scaled the initial amount by dividing it with 100 
        "buy_cost_pct": 0.0019, #IPOT has 0.19% buy cost
        "sell_cost_pct": 0.0029, #IPOT has 0.29% sell cost
        "state_space": state_space, 
        "stock_dim": stock_dimension, 
        "tech_indicator_list": config.TECHNICAL_INDICATORS_LIST, 
        "action_space": stock_dimension,
        "reward_scaling": 1e-4,
        "print_verbosity":5
    }
    
    rebalance_window = 63 # rebalance_window is the number of days to retrain the model
    validation_window = 63 # validation_window is the number of days to do validation and trading (e.g. if validation_window=63, then both validation and trading period will be 63 days)
    train_start = config.TRAIN_START
    train_end = config.TRAIN_END
    val_test_start = config.VAL_TEST_START
    val_test_end = config.VAL_TEST_END

    ensemble_agent = DRLEnsembleAgent(df=processed_full,
                    train_period=(train_start,train_end),
                    val_test_period=(val_test_start,val_test_end),
                    rebalance_window=rebalance_window, 
                    validation_window=validation_window, 
                    **env_kwargs)
    
    A2C_model_kwargs = {
                       'n_steps': 5,
                        'ent_coef': 0.01,
                        'learning_rate': 0.0005
                        }

    PPO_model_kwargs = {
                        "ent_coef":0.01,
                        "n_steps": 2048,
                        "learning_rate": 0.00025,
                        "batch_size": 128
                        }

    DDPG_model_kwargs = {
                        "action_noise":"ornstein_uhlenbeck",
                        "buffer_size": 50_000,
                        "learning_rate": 0.000005,
                        "batch_size": 128
                        }

    timesteps_dict = {'a2c' : 100_000, 
                    'ppo' : 100_000, 
                    'ddpg' : 50_000
                    }
    
    df_summary = ensemble_agent.run_ensemble_strategy(A2C_model_kwargs,
                                                 PPO_model_kwargs,
                                                 DDPG_model_kwargs,
                                                 timesteps_dict)
    
    
    unique_trade_date = processed_full[(processed_full.date > val_test_start)&(processed_full.date <= val_test_end)].date.unique()

    df_trade_date = pd.DataFrame({'datadate':unique_trade_date})

    df_account_value=pd.DataFrame()
    for i in range(rebalance_window+validation_window, len(unique_trade_date)+1,rebalance_window):
        temp = pd.read_csv('results/account_value_trade_{}_{}.csv'.format('ensemble',i))
        df_account_value = df_account_value.append(temp,ignore_index=True)
    sharpe=(252**0.5)*df_account_value.account_value.pct_change(1).mean()/df_account_value.account_value.pct_change(1).std()
    print('Sharpe Ratio: ',sharpe)
    df_account_value=df_account_value.join(df_trade_date[validation_window:].reset_index(drop=True))
    
    df_account_value.head()
    
    df_account_value.account_value.plot()
    
    print("==============Get Backtest Results===========")
    now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')

    perf_stats_all = backtest_stats(account_value=df_account_value)
    perf_stats_all = pd.DataFrame(perf_stats_all)
    
    
    print("==============Compare to IHSG===========")
    backtest_plot(df_account_value, 
                baseline_ticker = '^JKSE', 
                baseline_start = df_account_value.loc[0,'date'],
                baseline_end = df_account_value.loc[len(df_account_value)-1,'date'])
    
    print("==============Get Baseline Stats===========")
    baseline_perf_stats=get_baseline('^JKSE',
                                    baseline_start = df_account_value.loc[0,'date'],
                                    baseline_end = df_account_value.loc[len(df_account_value)-1,'date'])