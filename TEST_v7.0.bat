@echo off
echo ================================================================
echo  Profit Bot v7.0 - TEST MODE
echo ================================================================
echo.
echo [TEST ITEMS]
echo - Module import test
echo - Strategy object creation test
echo - Learning system test
echo - Bot object creation test
echo - Entry/Exit logic test (8 scenarios)
echo.
echo ----------------------------------------------------------------
echo Starting tests...
echo ----------------------------------------------------------------
echo.

python test_quick_v7.py

echo.
echo ----------------------------------------------------------------
echo Test completed!
echo ----------------------------------------------------------------
echo.
echo NEXT STEPS:
echo 1. If all tests pass -^> Run RUN_PAPER_v7.0.bat (Simulation)
echo 2. After sufficient simulation -^> Run RUN_LIVE_v7.0.bat (Live)
echo.
pause
