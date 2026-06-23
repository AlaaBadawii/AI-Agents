from ..memory import Memory

def test_memory():
    mem = Memory()
    
    mem.add_to_memory({
        "role": "user",
        "content": "list files"
    })

    print(mem.get_memory())

    mem.clear_memory()

    print(mem.get_memory())


if __name__ == "__main__":
    test_memory()
    print("All tests passed!")


