import time
import openai

class Agent:
    def __init__(self, key, filepaths = None, name = "ReaderV3", desc = "Extracts specific details about the data and precise analysis methodology from a particular scientific research paper.", instrs = "You are an expert in reading and understanding computational biology research papers. From a particular scientific research paper (contained in your knowledge base), you extract specific details about the data, analysis methodology, and procedures employed by the authors."):
        # Default is the Reader
        self.client = openai.OpenAI(api_key=key)
        if filepaths:
            assistant = self.client.beta.assistants.create(
                name=name,
                description=desc,
                instructions=instrs,
                model="gpt-3.5-turbo-0125",
                tools=[{"type": "file_search"}],
            )

            
            # Create a vector store caled "Financial Statements"
            vector_store = self.client.beta.vector_stores.create(name="KB")
            
            # Ready the files for upload to OpenAI
            file_streams = [open(path, "rb") for path in filepaths]
            
            # Use the upload and poll SDK helper to upload the files, add them to the vector store,
            # and poll the status of the file batch for completion.
            file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id, files=file_streams
            )
            
            assistant = self.client.beta.assistants.update(
                assistant_id=assistant.id,
                tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
            )
        else:
            assistant = self.client.beta.assistants.create(
                name=name,
                description=desc,
                instructions=instrs,
                model="gpt-4-turbo",
                tools=[{"type": "code_interpreter"}],
            )

            
        self.AID = assistant.id

    
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
        id = self.AID
        return self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=id,
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
    Prints a thread's messages in an easily readable visual format. 
    """
    def pretty_print(self, messages):
        print("# Messages")
        for m in messages:
            print(f"{m.role}: {m.content[0].text.value}")
        print()


    """
    Saves the full conversation as a textfile and returns it as a string.
    """
    def save_full_chat(self, outpath, thread):
        out_msg = ""
        all_messages = self.get_response(thread) 
        for m in all_messages:
            out_msg += f"{m.role}:\n{m.content[0].text.value}\n\n"
            if m.role == "assistant":
                out_msg += "\n\n"

        # Your pick of saving this as a pickle, text, json, etc
        # E.g. txt
        # Writing the string to a text file
        with open(outpath, "w") as file:
            file.write(out_msg)
        
        return out_msg

    """
    Saves the responses for each user prompt asked during the course of the full conversation as a textfile and returns it as a string.
    """
    def save_all_responses(self, outpath, thread):
        out_msg = ""
        all_messages = self.get_response(thread) 
        for m in all_messages:
            if m.role == "assistant":
                out_msg += f"{m.content[0].text.value}\n\n"

        with open(outpath, "w") as file:
            file.write(out_msg)
        
        return out_msg

    """
    Saves the response for the final user prompt asked as a textfile and returns it as a string.
    """
    def save_final_response(self, outpath, thread):
        all_messages = self.get_response(thread) 
        
        out_msg = all_messages.data[-1].content[0].text.value

        with open(outpath, "w") as file:
            file.write(out_msg)
        
        return out_msg
    
    """
    Gets the response for the final user prompt and returns it as a string.
    """
    def get_final_response(self, thread):
        all_messages = self.get_response(thread) 
        
        out_msg = all_messages.data[-1].content[0].text.value

        return out_msg