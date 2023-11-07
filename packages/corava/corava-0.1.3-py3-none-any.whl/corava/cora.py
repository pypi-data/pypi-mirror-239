import time
from corava.audio_util import speak, listen
from corava.openai_services import get_chatgpt_response, get_conversation_history
from corava.utilities import user_said_shutdown, user_said_sleep, log_message

cora_is_running = True
wake_words = ["cora", "kora", "quora", "korra", "kooora"]
sleeping = False

# the main conversation loop after wake-up word was detected
def run_conversation(initial_query, config):
    global cora_is_running
    initialized = False
    while True:
        # if we've already handled the initial query then continue the conversation and listen for the next prompt otherwise handle the initial query
        if initialized:
            user_query = listen(sleeping).lower()

            if user_said_sleep(user_query):
                # break out of the the loop go back to voice loop
                speak("okay, going to sleep.", config)    
                break
            if user_said_shutdown(user_query):
                # break out of the loop and let voice shutdown
                speak("okay, see you later.", config)
                cora_is_running = False
                break

            if not(user_query == ""):
                chatgpt_response = get_chatgpt_response(user_query, config)
                speak(chatgpt_response, config)
        else:
            initialized = True

            # if the user has woken up cora and asked to shutdown in the same sentance
            if user_said_shutdown(initial_query):
                # break out of the loop and let voice shutdown
                cora_is_running = False
                break
        
            chatgpt_response = get_chatgpt_response(initial_query, config)
            speak(chatgpt_response, config)

        # have a small pause between listening loops
        time.sleep(1)

def voice(config):
    while cora_is_running:
        global sleeping 
        sleeping = True
        print(log_message("SYSTEM", "sleeping."))

        user_said = listen(sleeping).lower()

        # look through the audio and if one of the wake-words have been detected start conversation
        for wake_word in wake_words:
            if wake_word in user_said:
                print(log_message("SYSTEM", f"wake-word detected: {wake_word}"))
                sleeping = False
                run_conversation(user_said, config)

    print(log_message("SYSTEM", "shutting down."))

# starts all the threads that run CORA. After threads have shutdown returns conversation history
def start(config):
    """
    starts the threads that are required to run cora

    Returns:
        list: the conversation history of the completed session.
    """
    voice(config)
    return get_conversation_history()