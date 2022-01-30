## ***Group Data & Analytics – Backend Assignment :***

_Clone the repository_ : git clone https://github.com/deepunahak/AdityaBirla-GDA-assignment.git
### _Pre-requisite for Flask app :_
__________________

      01. Python 3.x.x sholud be installed

      02. Open a command prompt or linux terminal

      03. Create a virtual environment

          RUN:  python -m venv your_env_name
            
      04. Activate virtual environment 

          RUN[Windows]: .\<you_env_name>\Script\activate
          RUN[Linux]: source ./<you_env_name>/bin/activate

      05. In terminal/command prompt Navigate to 
          <AdityaBirla-GDA-assignment>/<flask_app> directory.

          RUN: pip install -r requirements.txt
            
      06. To start the app go to AdityaBirla-GDA-assignment>/<flask_app> directory.
        
          RUN: python main.py

      [NOTE : Make sure start the application host: localhost & port:5000]
      

### _Pre-requisite for Django app :_
___________________

      01. Python 3.x.x sholud be installed

      02. Open a command prompt or linux terminal

      03. Create a virtual environment

          RUN:  python -m venv your_env_name
            
      04. Activate virtual environment 

          RUN[Windows]: .\<you_env_name>\Script\activate
          RUN[Linux]: source ./<you_env_name>/bin/activate

      05. In terminal/command prompt Navigate to 
          <AdityaBirla-GDA-assignment>/<django_gda_proj> directory.

          RUN: pip install -r requirements.txt
            
      06. To start the app go to <AdityaBirla-GDA-assignment>/<django_gda_proj> directory.
        
          RUN: python manage.py runserver

      [Note 1: Before start calling django endpoints make sure flask application is running]

      [Note 2: Django app server starts with default port 8000 and host as localhost make sure 
             while calling the RESTAPI's use url 'https://localhost:8000/<API ENDPOINTS HERE>]
