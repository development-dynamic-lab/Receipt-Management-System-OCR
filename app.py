from Backend.flask_app import run_app

##entry point
if __name__ == "__main__":
  try:
    run_app()
  except Exception as e:
    print(e)