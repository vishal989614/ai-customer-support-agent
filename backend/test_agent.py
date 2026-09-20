from agents.graph import build_support_graph


agent = build_support_graph()


question = "Where is my order?"


result = agent.invoke(
    {
        "question": question
    }
)


print("\nQUESTION:")
print(question)

print("\nCAPABILITY:")
print(result["capability"])

print("\nANSWER:")
print(result["answer"])