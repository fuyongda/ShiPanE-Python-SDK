# -*- coding: utf-8 -*-

import datetime

try:
    from shipane_sdk.client import Client
except:
    pass

try:
    from kuanke.user_space_api import *
except:
    pass


class JoinQuantExecutor(object):
    def __init__(self, **kwargs):
        if 'log' in globals():
            self._logger = log
        else:
            import logging
            self._logger = logging.getLogger()
        self._client = Client(self._logger, **kwargs)
        self._client_param = kwargs.get('client')
        self._order_id_map = dict()
        self._started_at = datetime.datetime.now()

    @property
    def client(self):
        return self._client

    @property
    def client(self):
        return self._client

    def execute(self, order):
        if order is None:
            self._logger.info('[实盘易] 委托为空，忽略下单请求')
            return

        if self.__is_expired(order):
            self._logger.info('[实盘易] 委托已过期，忽略下单请求')
            return

        try:
            action = 'BUY' if order.is_buy else 'SELL'
            actual_order = self._client.execute(self._client_param,
                                                action=action,
                                                symbol=order.security,
                                                price=order.price,
                                                amount=order.amount)
            self._order_id_map[order.order_id] = actual_order['id']
            return actual_order
        except Exception as e:
            self._logger.error("[实盘易] 下单异常：" + str(e))

    def cancel(self, order):
        if order is None:
            self._logger.info('[实盘易] 委托为空，忽略撤单请求')
            return

        try:
            order_id = order if isinstance(order, int) else order.order_id
            if order_id in self._order_id_map:
                self._client.cancel(self._client_param, self._order_id_map[order_id])
            else:
                self._logger.warning('[实盘易] 未找到对应的委托编号')
        except Exception as e:
            self._logger.error("[实盘易] 撤单异常：" + str(e))

    def __is_expired(self, order):
        return order.add_time < self._started_at
