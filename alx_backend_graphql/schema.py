import graphene

class Query(CRMQuery, graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL World!")

schema = graphene.Schema(query=Query)
