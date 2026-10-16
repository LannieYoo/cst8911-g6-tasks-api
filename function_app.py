import azure.functions as func

from functions.create_task import bp as create_task_bp
from functions.get_tasks import bp as get_tasks_bp

app = func.FunctionApp()

# One blueprint per team member. Add one line here for each new function file.
app.register_functions(create_task_bp)
app.register_functions(get_tasks_bp)
