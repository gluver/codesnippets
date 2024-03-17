function Set-Proxy {
    param (
        [string]$server,  # Proxy server address
        [int]$port        # Port number
    )
    $proxyPath = "{0}:{1}" -f $server,$port
    Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' -Name ProxyServer -Value $proxyPath
    Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' -Name ProxyEnable -Value 1


}

$local:proxyPort = 7890
$defaultGateway = (Get-NetRoute | Where-Object { $_.DestinationPrefix -eq '0.0.0.0/0' } | Select-Object -ExpandProperty NextHop)
$proxyPath = "{0}:{1}" -f $defaultGateway,$proxyPort
Write-Host "Proxy automatically set successfully to $proxyPath"
Set-Proxy -server ${defaultGateway} -port $proxyPort
