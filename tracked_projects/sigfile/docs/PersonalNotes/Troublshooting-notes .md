Start amd stop the app adn generate test data while LogicLens is the SUT Using standard "test"  cpmmadnd.

1. Run in venv to make sure not already runnimg :

(venv){promt}: % - pkill -f "flask run|python.*logiclens_manage.py" || true
 %

 or 

 pkill -f "flask run|python.*logiclens_manage.py" || true

 THEN verify : 
  ps aux | grep -E 'flask|python.*logiclens_manage.py' | grep -v grep

Then deactivate venev environemnt :

  (venv){promt}: % deactivate

  OR 

  (venv){promt}: % exit

  the (venv) should now be gone and you should be back to the regular promt.

  Verify that the app is not running :

  (promt): % ps aux | grep -E 'flask|python.*logiclens_manage.py' | grep -v grep

  If you see no output, the app is not running.

remove venv folder :

rm -rf venv backend/venv


2. set up a clean install of the Flask application which hosts the react frontend and the python backend and run all tests :

1. cd backend && python3 -m venv venv
2. source venv/bin/activate&& pip install -r requirements.txt

verify that we have only one virtual environment active and start the Flask application:

3. cd app && FLASK_APP=__init__.py FLASK_ENV=development flask run --host=0.0.0.0 --port=5050 > /tmp/flask.log 2>&1 & echo $! > /tmp/flask.pid && cd ../../ && echo "LogicLens started on port 5050. PID: $(cat /tmp/flask.pid)"




(venv){promt}: % cd backend && source venv/bin/activate && cd app && FLASK_APP=__init__.py FLASK_ENV=development flask run --host=0.0.0.0 --port=5050 > /tmp/flask.log 2>&1 & echo $! > /tmp/flask.pid && cd ../../ && echo "LogicLens started on port 5050. PID: $(cat /tmp/flask.pid)"

Output should be saomething like :

<ens started on port 5050. PID: $(cat /tmp/flask.pid)"
[1] 66121
LogicLens started on port 5050. PID: 66121
(venv){promt}: %

Wait for hte app to intitialize and then run the tests :

(venv){promt}: % python -m pytest tests/

Or for mock testing of the applicaiton ther eis a test test data generation script that will create mock test data  that is alos viewable form the frontend allocation TO use this script run :

(venv){promt}: % python generate_test_data.py

This will create a new folder in the backend directory called test_data which will contain the mock test data.


the ourput should be something like :

Generating mock test data...
Test data generation complete.  

This has generated:
4 test suites (API Tests, Frontend Tests, Integration Tests, Performance Tests)
10 test cases per suite with a mix of PASSED, FAILED, and SKIPPED results
20 system metrics snapshots with randomized data
All this data should now be visible in the LogicLens dashboard
To access the UI, visit http://localhost:5050 in your browser, and you should be able to see all the test data we just generated.
If you need to stop the application later, you can use:

(venv){promt}: % pkill -f "flask run|python.*logiclens_manage.py" || true   

This will stop the Flask application and the LogicLens service.




    Addtional notes :
    Chacking running python applitcations :
    ps aux | grep -E 'python|flask|logiclens_manage'

    To stop all running python applications:
    pkill -f "python|flask|logiclens_manage"

To check the status of a port you can sue the lsof command :

lsof -i :5050

To check the CORS configuration backend/app/_init_.py :

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "X-API-Key"]
    }
}) 

USe the Curl command to check the CORS configuration :

curl -X OPTIONS -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: Content-Type" -v http://localhost:5050/api/test
