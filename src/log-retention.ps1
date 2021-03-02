$Destination = $args[0]
Get-ChildItem -Path $Destination\*log -Recurse | where{-not $_.PsIsContainer}| sort CreationTime -desc| select -Skip 4| Remove-Item -Force