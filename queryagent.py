
import time
import openai

class QueryAgent:
    def __init__(self, client, aid):
        """
        Initialize the QueryAgent with an openai client.
        """
        self.client = client
        self.assistant_id = aid
    
    """
    Blocks program execution till the specified run has completed.
    """
    def wait_on_run(self, run, thread):
        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(1.0)
        return run


    """
    Sends the specified user message to the given thread using the assistant of choice.
    """
    def submit_message(self, thread, user_message):
        self.client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_message
        )
        return self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id,
        )


    """
    Obtains the assistant response(s) from the thread specified.
    """
    def get_response(self, thread):
        return self.client.beta.threads.messages.list(thread_id=thread.id, order="asc")



    """
    Creates and runs a thread with an inital user message using the specified assistant. 
    """
    def create_thread_and_run(self, user_message):
        thread = self.client.beta.threads.create()
        run = self.submit_message(thread, user_message)
        return thread, run

    """
    Creates a thread. 
    """
    def create_thread(self):
        thread = self.client.beta.threads.create()
        return thread


    """
    Prints a thread's messages in an easily readable visual format. 
    """
    def pretty_print(self, messages):
        print("# Messages")
        for m in messages:
            print(f"{m.role}: {m.content[0].text.value}")
        print()


    """
    Prints the specified openai object in a visually easy to read json format.
    """
    def print_obj(self, obj):
        try:
            print(obj.model_dump_json(indent=1))
        except:
            print('Error: unrecognized type')