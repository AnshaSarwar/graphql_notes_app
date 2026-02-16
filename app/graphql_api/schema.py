import strawberry
from graphql_api.queries import Query
from graphql_api.mutations import Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)
