#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White
#                                                                              
# PyGithub is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.                                                           
#                                                                              
# PyGithub is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS   
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#                                                                      
# You should have received a copy of the GNU Lesser General Public License
# along with PyGithub. If not, see <http://www.gnu.org/licenses/>.

from . import api_exceptions
from .api_objects import NotSet, Price, Product, Store
from .requester import Requester
from .paginated import PaginatedList

DEFAULT_BASE_URL = "http://www.oregonliquorprices.com"

class PyOLP:

    def __init__(self, base_url=DEFAULT_BASE_URL):

        self.__requester = Requester(base_url)

    def get_product(self, id=NotSet):
        """
        :calls: `GET /api/v1/product/`
        :param code: string
        :rtype: :class: `product.Product`
        """
        assert id is NotSet or isinstance(id, str), id
        headers, data = self.__requester.requestJsonAndCheck(
            "/api/v1/product/" + str(id) + "/"
        )
        return Product(self.__requester, headers, data)

    def get_products(self, code=NotSet,
            on_sale=NotSet, proof=NotSet,
            status=NotSet, title=NotSet):
        """
        :calls: `GET /api/v1/product/`
        :param code: string
        :param on_sale: bool
        :param proof: float
        :param status: string
        :param title: string
        :rtype: :class: `paginated.PaginatedList`
        """
        assert code is NotSet or isinstance(code, str), code
        assert on_sale is NotSet or isinstance(on_sale, bool), on_sale
        assert proof is NotSet or isinstance(proof, (int, float)), proof
        assert status is NotSet or isinstance(status, str), status
        assert title is NotSet or isinstance(title, str), title
        url_parameters = dict()
        if code is not NotSet:
            url_parameters["code"] = code
        if on_sale is not NotSet:
            url_parameters["on_sale"] = on_sale
        if proof is not NotSet:
            url_parameters["proof"] = proof
        if status is not NotSet:
            url_parameters["status"] = status
        if title is not NotSet:
            url_parameters["title"] = title
        return PaginatedList(
            Product,
            self.__requester,
            '/api/v1/product/',
            url_parameters
        )

    def get_store(self, id=NotSet):
        """
        :calls: `GET /api/v1/store/`
        :param id: string
        :rtype: :class: `store.Store`
        """
        assert id is NotSet or isinstance(id, str), id
        headers, data = self.__requester.requestJsonAndCheck(
            "/api/v1/store/" + str(id) + "/"
        )
        return Store(self.__requester, headers, data)

    def get_stores(self):
        """
        :calls: `GET /api/v1/store/`
        :rtype: :class: `paginated.PaginatedList`
        """
        return PaginatedList(
            Store,
            self.__requester,
            '/api/v1/store/'
        )

    def get_price(self, id=NotSet):
        """
        :calls: `GET /api/v1/price/`
        :param id: string
        :rtype: :class: `price.Price`
        """
        assert id is NotSet or isinstance(id, str), id
        headers, data = self.__requester.requestJsonAndCheck(
            "/api/v1/price/" + str(id) + "/"
        )
        return Price(self.__requester, headers, data)

    def get_prices(self, product_id=NotSet):
        """
        :calls: `GET /api/v1/price/`
        :rtype: :class: `paginated.PaginatedList`
        """
        assert product_id is NotSet or isinstance(product_id, str), product_id
        url_parameters = dict()
        if product_id is not NotSet:
            url_parameters["product"] = product_id
        return PaginatedList(
            Price,
            self.__requester,
            '/api/v1/price/',
            url_parameters
        )
