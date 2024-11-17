@echo off
echo Running all tests...

python manage.py test apps.accounts.tests.testAuthentication
if %errorlevel% neq 0 (
    echo Error in testAuthentication
    exit /b %errorlevel%
)

python manage.py test apps.accounts.tests.testClientRegister
if %errorlevel% neq 0 (
    echo Error in testClientRegister
    exit /b %errorlevel%
)

python manage.py test apps.accounts.tests.testFreelancerProfileSettings
if %errorlevel% neq 0 (
    echo Error in testFreelancerProfileSettings
    exit /b %errorlevel%
)

python manage.py test apps.accounts.tests.testFreelancerRegister
if %errorlevel% neq 0 (
    echo Error in testFreelancerRegister
    exit /b %errorlevel%
)

python manage.py test apps.accounts.tests.testLandpage
if %errorlevel% neq 0 (
    echo Error in testLandpage
    exit /b %errorlevel%
)

python manage.py test apps.accounts.tests.testLogin
if %errorlevel% neq 0 (
    echo Error in testLogin
    exit /b %errorlevel%
)

python manage.py test apps.accounts.tests.testRecoverMyAccount
if %errorlevel% neq 0 (
    echo Error in testRecoverMyAccount
    exit /b %errorlevel%
)

python manage.py test apps.accounts.tests.testUrls
if %errorlevel% neq 0 (
    echo Error in testUrls
    exit /b %errorlevel%
)

python manage.py test apps.communications.tests.testUrls
if %errorlevel% neq 0 (
    echo Error in testUrls
    exit /b %errorlevel%
)

python manage.py test apps.communications.tests.testAuthentication
if %errorlevel% neq 0 (
    echo Error in testAuthentication
    exit /b %errorlevel%
)


python manage.py test apps.projects.tests.testBrowseProjects
if %errorlevel% neq 0 (
    echo Error in testBrowseProjects
    exit /b %errorlevel%
)

python manage.py test apps.projects.tests.testAddDeliverables
if %errorlevel% neq 0 (
    echo Error in testAddDeliverables
    exit /b %errorlevel%
)
python manage.py test apps.projects.tests.testAddMilestoneDeliverables
if %errorlevel% neq 0 (
    echo Error in testAddMilestoneDeliverables
    exit /b %errorlevel%
)
python manage.py test apps.projects.tests.testCreateAndUpdateProjects
if %errorlevel% neq 0 (
    echo Error in testCreateAndUpdateProjects
    exit /b %errorlevel%
)
python manage.py test apps.projects.tests.testDeleteDeliverable
if %errorlevel% neq 0 (
    echo Error in testDeleteDeliverable
    exit /b %errorlevel%
)
python manage.py test apps.projects.tests.testDeleteMilestone
if %errorlevel% neq 0 (
    echo Error in testDeleteMilestone
    exit /b %errorlevel%
)
python manage.py test apps.accounts.tests.testClientRegister
if %errorlevel% neq 0 (
    echo Error in testClientRegister
    exit /b %errorlevel%
)

python manage.py test apps.projects.tests.testClientRegister
if %errorlevel% neq 0 (
    echo Error in testClientRegister
    exit /b %errorlevel%
)

python manage.py test apps.projects.tests.testFreelancerProfileSettings
if %errorlevel% neq 0 (
    echo Error in testFreelancerProfileSettings
    exit /b %errorlevel%
)

python manage.py test apps.projects.tests.testGateWay
if %errorlevel% neq 0 (
    echo Error in testGateWay
    exit /b %errorlevel%
)

python manage.py test apps.projects.tests.test_projects
if %errorlevel% neq 0 (
    echo Error in test_projects
    exit /b %errorlevel%
)

python manage.py test apps.dashboard.tests.testDashboard
if %errorlevel% neq 0 (
    echo Error in testDashboard
    exit /b %errorlevel%
)

python manage.py test apps.dashboard.tests.testAuthentication
if %errorlevel% neq 0 (
    echo Error in testAuthentication
    exit /b %errorlevel%
)

python manage.py test apps.dashboard.tests.testUrls
if %errorlevel% neq 0 (
    echo Error in testUrls
    exit /b %errorlevel%
)

python manage.py test apps.notifications.tests.testAuthentication
if %errorlevel% neq 0 (
    echo Error in testAuthentication
    exit /b %errorlevel%
)

python manage.py test apps.notifications.tests.testUrls
if %errorlevel% neq 0 (
    echo Error in testUrls
    exit /b %errorlevel%
)

python manage.py test apps.projects.tests.testUrls
if %errorlevel% neq 0 (
    echo Error in testUrls
    exit /b %errorlevel%
)

python manage.py test apps.communications.tests.testCreateChat
if %errorlevel% neq 0 (
    echo Error in testCreateChat
    exit /b %errorlevel%
)

python manage.py test apps.communications.tests.testMessage
if %errorlevel% neq 0 (
    echo Error in testMessage
    exit /b %errorlevel%
)

python manage.py test apps.communications.tests.testMessageHome
if %errorlevel% neq 0 (
    echo Error in testMessageHome
    exit /b %errorlevel%
)


echo All tests completed.
