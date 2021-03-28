"""
Train model using FinRL
"""

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = str(parent.parent).replace("\\", "\\\\")
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
from finrl.trade.backtest import BackTestStats, BaselineStats, BackTestPlot

from pprint import pprint

import sys
sys.path.append("../FinRL-Library")

import itertools

from drl import config as cfg

import os
if not os.path.exists("./" + cfg.config['DATA_SAVE_DIR']):
    os.makedirs("./" + cfg.config['DATA_SAVE_DIR'])
if not os.path.exists("./" + cfg.config['TRAINED_MODEL_DIR']):
    os.makedirs("./" + cfg.config['TRAINED_MODEL_DIR'])
if not os.path.exists("./" + cfg.config['TENSORBOARD_LOG_DIR']):
    os.makedirs("./" + cfg.config['TENSORBOARD_LOG_DIR'])
if not os.path.exists("./" + cfg.config['RESULTS_DIR']):
    os.makedirs("./" + cfg.config['RESULTS_DIR'])
    
from ohlc import preprocess as prep

if __name__ == "__main__":
    # df = prep.preprocess(size=500, symbols=['AAPL'], to_csv=True)
    
    # ! tmp : remove later
    # df['turbulence'] = np.random.randint(1, 10, size=len(df))

    df = YahooDownloader(start_date = config.START_DATE,
                        end_date = '2021-01-19',
                        ticker_list = ['AAPL', 'IBM', 'TSLA', 'AMZN', 'FB']).fetch_data()

    df.sort_values(['date','tic']).head()
    
    fe = FeatureEngineer(
                    use_technical_indicator=True,
                    tech_indicator_list = ['macd', 'boll_ub', 'boll_lb', 'rsi_30', 'cci_30', 'dx_30', 'close_30_sma', 'close_60_sma'],
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
    state_space = 1 + 2*stock_dimension + len(['macd', 'boll_ub', 'boll_lb', 'rsi_30', 'cci_30', 'dx_30', 'close_30_sma', 'close_60_sma'])*stock_dimension
    print(f"Stock Dimension: {stock_dimension}, State Space: {state_space}")

    # stock_dimension = len(df.columns) - 1
    # state_space = 1 + stock_dimension

    # env_kwargs = {
    #     "hmax": 100, 
    #     "initial_amount": 50_000_000/100, #Since in Indonesia the minimum number of shares per trx is 100, then we scaled the initial amount by dividing it with 100 
    #     "buy_cost_pct": 0.0019, #IPOT has 0.19% buy cost
    #     "sell_cost_pct": 0.0029, #IPOT has 0.29% sell cost
    #     "state_space": state_space,
    #     "tech_indicator_list": ["volume_adi", "volume_obv", "volume_cmf", "volume_fi", "volume_mfi", "volume_em", "volume_sma_em", "volume_vpt", "volume_nvi", "volume_vwap volatility_atr", "volatility_bbm", "volatility_bbh", "volatility_bbl", "volatility_bbw", "volatility_bbp", "volatility_bbhi", "volatility_bbli", "volatility_kcc", "volatility_kch", "volatility_kcl", "volatility_kcw", "volatility_kcp", "volatility_kchi", "volatility_kcli", "volatility_dcl", "volatility_dch", "volatility_dcm", "volatility_dcw", "volatility_dcp", "volatility_ui", "trend_macd", "trend_macd_signal trend_macd_diff", "trend_sma_fast", "trend_sma_slow", "trend_ema_fast", "trend_ema_slow", "trend_adx", "trend_adx_pos", "trend_adx_neg", "trend_vortex_ind_pos", "trend_vortex_ind_neg", "trend_vortex_ind_diff", "trend_trix", "trend_mass_index", "trend_cci", "trend_dpo", "trend_kst", "trend_kst_sig", "trend_kst_diff", "trend_ichimoku_conv", "trend_ichimoku_base", "trend_ichimoku_a", "trend_ichimoku_b", "trend_visual_ichimoku_a trend_visual_ichimoku_b trend_aroon_up", "trend_aroon_down", "trend_aroon_ind", "trend_psar_up", "trend_psar_down", "trend_psar_up_indicator trend_psar_down_indicator", "trend_stc", "momentum_rsi", "momentum_stoch_rsi", "momentum_stoch_rsi_k", "momentum_stoch_rsi_d", "momentum_tsi", "momentum_uo momentum_stoch", "momentum_stoch_signal", "momentum_wr momentum_ao momentum_kama", "momentum_roc", "momentum_ppo", "momentum_ppo_signal", "momentum_ppo_hist others_dr", "others_dlr", "others_cr"],
    #     "stock_dim": 1,
    #     "action_space": 1, 
    #     "reward_scaling": 1e-4,
    #     "print_verbosity":5
    # }
    
    env_kwargs = {
        "hmax": 100, 
        "initial_amount": 50_000_000/100, #Since in Indonesia the minimum number of shares per trx is 100, then we scaled the initial amount by dividing it with 100 
        "buy_cost_pct": 0.0019, #IPOT has 0.19% buy cost
        "sell_cost_pct": 0.0029, #IPOT has 0.29% sell cost
        "state_space": state_space, 
        "stock_dim": stock_dimension, 
        "tech_indicator_list": ['macd', 'boll_ub', 'boll_lb', 'rsi_30', 'cci_30', 'dx_30', 'close_30_sma', 'close_60_sma'], 
        "action_space": stock_dimension, 
        "reward_scaling": 1e-4,
        "print_verbosity":5
    }
    
    rebalance_window = 63 # rebalance_window is the number of days to retrain the model
    validation_window = 63 # validation_window is the number of days to do validation and trading (e.g. if validation_window=63, then both validation and trading period will be 63 days)
    train_start = '2000-01-01'
    train_end = '2019-01-01'
    val_test_start = '2019-01-01'
    val_test_end = '2021-01-18'

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

    perf_stats_all = BackTestStats(account_value=df_account_value)
    perf_stats_all = pd.DataFrame(perf_stats_all)
    
    
    print("==============Compare to IHSG===========")
    BackTestPlot(df_account_value, 
                baseline_ticker = '^JKSE', 
                baseline_start = df_account_value.loc[0,'date'],
                baseline_end = df_account_value.loc[len(df_account_value)-1,'date'])
    
    print("==============Get Baseline Stats===========")
    baseline_perf_stats=BaselineStats('^JKSE',
                                    baseline_start = df_account_value.loc[0,'date'],
                                    baseline_end = df_account_value.loc[len(df_account_value)-1,'date'])