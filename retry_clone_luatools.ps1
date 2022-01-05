#script from https://anduin.aiursoft.com/post/2021/8/16/the-simplest-way-to-retry-in-powershell
$attempt = 0
do {
    try {
        # Do something that has a high possiblity to crash.
        git clone $env:LUATOOLS2REPO

        if (-not $LASTEXITCODE) {
             $success = $true
        } else {
            throw "Transient error. LASTEXITCODE is $LASTEXITCODE."
        }
    }
    catch {
        if ($attempt -eq 10) {
            # You can do some extra logging here.
            Write-Error "Task failed. With all $attempt attempts. Error: $($Error[0])"
            throw
        }

        Write-Host "Task failed. Attempt $attempt. Will retry in next $(5 * $attempt) seconds. Error: $($Error[0])" -ForegroundColor Yellow
        Start-Sleep -Seconds $(5 * $attempt)
    }
    
    $attempt++
    
} until($success)
