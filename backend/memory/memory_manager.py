from memory.conversation import ConversationMemory


memory = ConversationMemory()


def save_attempt(

    query,

    reason,

    action

):

    memory.add(

        "reflection",

        {

            "query": query,

            "reason": reason,

            "action": action

        }

    )


def get_memory():

    return memory.get()


def clear_memory():

    memory.clear()