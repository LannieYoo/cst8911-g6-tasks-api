import azure.functions as func

from functions.create_task import bp as create_task_bp
from functions.get_tasks import bp as get_tasks_bp
from functions.get_task import bp as get_task_bp
from functions.update_task import bp as update_task_bp

app = func.FunctionApp()

# One blueprint per team member. Add one line here for each new function file.
app.register_functions(create_task_bp)
app.register_functions(get_tasks_bp)
app.register_functions(get_task_bp)
app.register_functions(update_task_bp)
