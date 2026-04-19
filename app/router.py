from semantic_router import Route, SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

faq = Route(
    name='faq',
    utterances=[
        "What is the return policy of the products?",
        "Do I get a discount with HDFC credit card?",
        "How can I track my orders?",
        "What modes of payment are accepted?",
        "How long does it take to process a refund?"
    ],
    score_threshold=0.3
)

sql = Route(
    name='sql',
    utterances=[
        "I want to buy nike shoes that have 50\% \discount",
        "Are there any shoes under Rs.3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
    ],
    score_threshold=0.3
)

small_talk = Route(
    name='small_talk',
    utterances=[
        "How are you?",
        "What is your name?",
        "Are you a robot?",
        "What are you?",
        "What do you do?",
    ]
)


router = SemanticRouter(routes=[faq, sql, small_talk], encoder=encoder, auto_sync="local")

if __name__ == "__main__":
    print(router("Whats your policy on on defective products?").name)
    print(router("Do you take cash as a payment?").name)
    print(router("Pink puma shoes in range 5000-10000").name)