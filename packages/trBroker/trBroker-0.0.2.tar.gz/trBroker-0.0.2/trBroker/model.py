# #import requests
# #from metaapi_cloud_sdk import MetaApi, MetaStats

# from pydantic import BaseModel, Field, validator
# from datetime import datetime
# from pydantic.types import conint
# # struct tr_br_TradeRequest
# #   {
# #    ENUM_TRADE_REQUEST_ACTIONS    action;           ## Trade operation type
# #    ulong                         magic;            ## Expert Advisor ID (magic number)
# #    ulong                         order;            ## Order ticket
# #    string                        symbol;           ## Trade symbol
# #    double                        volume;           ## Requested volume for a deal in lots
# #    double                        price;            ## Pricea
# #    double                        stoplimit;        ## StopLimit level of the order
# #    double                        sl;               ## Stop Loss level of the order
# #    double                        tp;               ## Take Profit level of the order
# #    ulong                         deviation;        ## Maximal possible deviation from the requested price
# #    ENUM_ORDER_TYPE               type;             ## Order type
# #    ENUM_ORDER_TYPE_FILLING       type_filling;     ## Order execution type
# #    ENUM_ORDER_TYPE_TIME          type_time;        ## Order expiration type
# #    datetime                      expiration;       ## Order expiration time (for the orders of ORDER_TIME_SPECIFIED type)
# #    string                        comment;          ## Order comment
# #    ulong                         position;         ## Position ticket
# #    ulong                         position_by;      ## The ticket of an opposite position
# #   };

# class TRADE_REQUEST_ACTIONS:
#     pass

# class ORDER_TYPE_FILLING:
#     pass

# class ORDER_TYPE_TIME:
#     pass
# class ulong(BaseModel):
#     ulong_variable: conint(ge=0)

# class TR_br_TradeRequest:
#     action : TRADE_REQUEST_ACTIONS
#     type:ORDER_TYPE_FILLING
#     type_filling: ORDER_TYPE_FILLING
#     type_time:ORDER_TYPE_TIME
    
#     magic: conint(ge=0)
#     order: conint(ge=0)
#     symbol: str
#     volume: float
#     price: float
#     stoplimit: float
#     stopLoss: float
#     TakeProfitLevel: float
#     deviation: float
#     expiration:datetime
#     comment: str
#     position: int
#     position_by:int
class main:
    def __init__(Self):
        pass
    def start(self):
        return True