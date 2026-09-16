$ErrorActionPreference = "Stop"
$location = "centralindia"
$stateRg = "svv-tfstate-rg"
$stateSa = "svvtfstate$((Get-Random -Minimum 10000 -Maximum 99999))"
az group create --name $stateRg --location $location | Out-Null
az storage account create --name $stateSa --resource-group $stateRg --location $location --sku Standard_LRS --kind StorageV2 --min-tls-version TLS1_2 --allow-blob-public-access false | Out-Null
az storage container create --name tfstate --account-name $stateSa --auth-mode login | Out-Null
Write-Host "TF_STATE_STORAGE_ACCOUNT=$stateSa"
