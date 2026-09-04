from rag.rag_chain import answer_question


question = "Who is the CEO of your company?"

answer = answer_question(question)

print("\nQUESTION:")
print(question)

print("\nAI ANSWER:")
print(answer)