# src


* [src package](src.md)


    * [Submodules](src.md#submodules)


    * [src.client module](src.md#module-src.client)


        * [`SxcApiClient`](src.md#src.client.SxcApiClient)


            * [`SxcApiClient.cancel_market_orders()`](src.md#src.client.SxcApiClient.cancel_market_orders)


            * [`SxcApiClient.cancel_order()`](src.md#src.client.SxcApiClient.cancel_order)


            * [`SxcApiClient.generate_ln_invoice()`](src.md#src.client.SxcApiClient.generate_ln_invoice)


            * [`SxcApiClient.generate_new_address()`](src.md#src.client.SxcApiClient.generate_new_address)


            * [`SxcApiClient.get_order()`](src.md#src.client.SxcApiClient.get_order)


            * [`SxcApiClient.get_price()`](src.md#src.client.SxcApiClient.get_price)


            * [`SxcApiClient.get_user_info()`](src.md#src.client.SxcApiClient.get_user_info)


            * [`SxcApiClient.list_addresses()`](src.md#src.client.SxcApiClient.list_addresses)


            * [`SxcApiClient.list_balances()`](src.md#src.client.SxcApiClient.list_balances)


            * [`SxcApiClient.list_fees()`](src.md#src.client.SxcApiClient.list_fees)


            * [`SxcApiClient.list_market_history()`](src.md#src.client.SxcApiClient.list_market_history)


            * [`SxcApiClient.list_markets()`](src.md#src.client.SxcApiClient.list_markets)


            * [`SxcApiClient.list_order_book()`](src.md#src.client.SxcApiClient.list_order_book)


            * [`SxcApiClient.list_orders_by_codes()`](src.md#src.client.SxcApiClient.list_orders_by_codes)


            * [`SxcApiClient.list_pending_orders()`](src.md#src.client.SxcApiClient.list_pending_orders)


            * [`SxcApiClient.list_prices()`](src.md#src.client.SxcApiClient.list_prices)


            * [`SxcApiClient.list_trades()`](src.md#src.client.SxcApiClient.list_trades)


            * [`SxcApiClient.list_transactions()`](src.md#src.client.SxcApiClient.list_transactions)


            * [`SxcApiClient.list_wallets()`](src.md#src.client.SxcApiClient.list_wallets)


            * [`SxcApiClient.place_order()`](src.md#src.client.SxcApiClient.place_order)


            * [`SxcApiClient.scroll_market_history_by_granularity()`](src.md#src.client.SxcApiClient.scroll_market_history_by_granularity)


            * [`SxcApiClient.send_request()`](src.md#src.client.SxcApiClient.send_request)


            * [`SxcApiClient.withdraw()`](src.md#src.client.SxcApiClient.withdraw)


    * [src.constants module](src.md#module-src.constants)


        * [`MarketHistoryIntervals`](src.md#src.constants.MarketHistoryIntervals)


            * [`MarketHistoryIntervals.DAYS_1`](src.md#src.constants.MarketHistoryIntervals.DAYS_1)


            * [`MarketHistoryIntervals.DAYS_3`](src.md#src.constants.MarketHistoryIntervals.DAYS_3)


            * [`MarketHistoryIntervals.DAYS_7`](src.md#src.constants.MarketHistoryIntervals.DAYS_7)


            * [`MarketHistoryIntervals.HOURS_1`](src.md#src.constants.MarketHistoryIntervals.HOURS_1)


            * [`MarketHistoryIntervals.HOURS_12`](src.md#src.constants.MarketHistoryIntervals.HOURS_12)


            * [`MarketHistoryIntervals.HOURS_6`](src.md#src.constants.MarketHistoryIntervals.HOURS_6)


            * [`MarketHistoryIntervals.MINUTES_1`](src.md#src.constants.MarketHistoryIntervals.MINUTES_1)


            * [`MarketHistoryIntervals.MINUTES_30`](src.md#src.constants.MarketHistoryIntervals.MINUTES_30)


            * [`MarketHistoryIntervals.MINUTES_5`](src.md#src.constants.MarketHistoryIntervals.MINUTES_5)


        * [`OrderTypes`](src.md#src.constants.OrderTypes)


            * [`OrderTypes.BUY`](src.md#src.constants.OrderTypes.BUY)


            * [`OrderTypes.SELL`](src.md#src.constants.OrderTypes.SELL)


        * [`TransactionTypes`](src.md#src.constants.TransactionTypes)


            * [`TransactionTypes.DEPOSITS`](src.md#src.constants.TransactionTypes.DEPOSITS)


            * [`TransactionTypes.DEPOSITS_BY_ADDRESS_ID`](src.md#src.constants.TransactionTypes.DEPOSITS_BY_ADDRESS_ID)


            * [`TransactionTypes.DEPOSITS_WITHDRAWALS`](src.md#src.constants.TransactionTypes.DEPOSITS_WITHDRAWALS)


            * [`TransactionTypes.TRADES_BY_ORDER_CODE`](src.md#src.constants.TransactionTypes.TRADES_BY_ORDER_CODE)


            * [`TransactionTypes.TRANSACTIONS`](src.md#src.constants.TransactionTypes.TRANSACTIONS)


            * [`TransactionTypes.WITHDRAWALS`](src.md#src.constants.TransactionTypes.WITHDRAWALS)


        * [`WithdrawalDestinationTypes`](src.md#src.constants.WithdrawalDestinationTypes)


            * [`WithdrawalDestinationTypes.CRYPTO_ADDRESS`](src.md#src.constants.WithdrawalDestinationTypes.CRYPTO_ADDRESS)


            * [`WithdrawalDestinationTypes.LIGHTNING_NETWORK_INVOICE`](src.md#src.constants.WithdrawalDestinationTypes.LIGHTNING_NETWORK_INVOICE)


            * [`WithdrawalDestinationTypes.USER_EMAIL_ADDRESS`](src.md#src.constants.WithdrawalDestinationTypes.USER_EMAIL_ADDRESS)


    * [src.exceptions module](src.md#module-src.exceptions)


        * [`SxcAnotherOrderIsInProcessError`](src.md#src.exceptions.SxcAnotherOrderIsInProcessError)


        * [`SxcApiError`](src.md#src.exceptions.SxcApiError)


        * [`SxcAuthDataMissingError`](src.md#src.exceptions.SxcAuthDataMissingError)


        * [`SxcInvalidDestinationTypeError`](src.md#src.exceptions.SxcInvalidDestinationTypeError)


        * [`SxcInvalidHashError`](src.md#src.exceptions.SxcInvalidHashError)


        * [`SxcInvalidKeyOrNonceError`](src.md#src.exceptions.SxcInvalidKeyOrNonceError)


        * [`SxcInvalidMarketError`](src.md#src.exceptions.SxcInvalidMarketError)


        * [`SxcMarketHistoryError`](src.md#src.exceptions.SxcMarketHistoryError)


        * [`SxcNoOrderCodeReturnedError`](src.md#src.exceptions.SxcNoOrderCodeReturnedError)


        * [`SxcNotEnoughBalanceError`](src.md#src.exceptions.SxcNotEnoughBalanceError)


        * [`SxcNotEnoughPermissionError`](src.md#src.exceptions.SxcNotEnoughPermissionError)


        * [`SxcOrderNotExistsError`](src.md#src.exceptions.SxcOrderNotExistsError)


        * [`SxcTooManyOrdersError`](src.md#src.exceptions.SxcTooManyOrdersError)


        * [`SxcUnsupportedCurrencyError`](src.md#src.exceptions.SxcUnsupportedCurrencyError)


        * [`raise_by_response()`](src.md#src.exceptions.raise_by_response)


    * [src.request_params module](src.md#module-src.request_params)


        * [`SxcApiRequestParams`](src.md#src.request_params.SxcApiRequestParams)


            * [`SxcApiRequestParams.access_key`](src.md#src.request_params.SxcApiRequestParams.access_key)


            * [`SxcApiRequestParams.auth_required`](src.md#src.request_params.SxcApiRequestParams.auth_required)


            * [`SxcApiRequestParams.headers`](src.md#src.request_params.SxcApiRequestParams.headers)


            * [`SxcApiRequestParams.method`](src.md#src.request_params.SxcApiRequestParams.method)


            * [`SxcApiRequestParams.nonce`](src.md#src.request_params.SxcApiRequestParams.nonce)


            * [`SxcApiRequestParams.payload`](src.md#src.request_params.SxcApiRequestParams.payload)


            * [`SxcApiRequestParams.payload_auth_injected`](src.md#src.request_params.SxcApiRequestParams.payload_auth_injected)


            * [`SxcApiRequestParams.payload_auth_injected_json`](src.md#src.request_params.SxcApiRequestParams.payload_auth_injected_json)


            * [`SxcApiRequestParams.payload_json`](src.md#src.request_params.SxcApiRequestParams.payload_json)


            * [`SxcApiRequestParams.request_args`](src.md#src.request_params.SxcApiRequestParams.request_args)


            * [`SxcApiRequestParams.secret_key`](src.md#src.request_params.SxcApiRequestParams.secret_key)


            * [`SxcApiRequestParams.url`](src.md#src.request_params.SxcApiRequestParams.url)


    * [Module contents](src.md#module-src)
