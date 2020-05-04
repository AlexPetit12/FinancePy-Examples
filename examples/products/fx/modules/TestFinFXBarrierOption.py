# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 16:51:05 2016

@author: Dominic O'Kane
"""

from financepy.models.FinProcessSimulator import FinProcessTypes
from financepy.models.FinProcessSimulator import FinGBMNumericalScheme
from financepy.products.fx.FinFXBarrierOption import FinFXBarrierTypes
from financepy.products.fx.FinFXBarrierOption import FinFXBarrierOption
from financepy.products.fx.FinFXModelTypes import FinFXModelBlackScholes
from financepy.market.curves.FinFlatCurve import FinFlatCurve
from financepy.finutils.FinDate import FinDate

###############################################################################


def test_FinFXBarrierOption():

    valueDate = FinDate(2015, 1, 1)
    expiryDate = FinDate(2016, 1, 1)
    spotFXRate = 100.0
    currencyPair = "USDJPY"
    volatility = 0.20
    domInterestRate = 0.05
    forInterestRate = 0.02
    optionType = FinFXBarrierTypes.DOWN_AND_OUT_CALL
    notional = 100.0
    notionalCurrency = "USD"

    drift = domInterestRate - forInterestRate
    scheme = FinGBMNumericalScheme.ANTITHETIC
    processType = FinProcessTypes.GBM
    domDiscountCurve = FinFlatCurve(valueDate, domInterestRate)
    forDiscountCurve = FinFlatCurve(valueDate, forInterestRate)
    model = FinFXModelBlackScholes(volatility)

    ###########################################################################

    import time
    start = time.time()
    numObservationsPerYear = 100

    print("Type", "K", "B", "S", "Value", "ValueMC", "Diff", "TIME")

    for optionType in FinFXBarrierTypes:
        for spotFXRate in range(80, 130, 10):
            B = 110.0
            K = 100.0

            option = FinFXBarrierOption(expiryDate, K, currencyPair,
                                        optionType, B,
                                        numObservationsPerYear,
                                        notional, notionalCurrency)

            value = option.value(valueDate, spotFXRate,
                                 domDiscountCurve, forDiscountCurve, model)

            start = time.time()
            modelParams = (spotFXRate, drift, volatility, scheme)
            valueMC = option.valueMC(valueDate, spotFXRate,
                                     domInterestRate, processType,
                                     modelParams)

            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value

            print(optionType, K, B, spotFXRate, value, valueMC,
                            diff, timeElapsed)

        for spotFXRate in range(80, 130, 10):
            B = 100.0
            K = 110.0

            option = FinFXBarrierOption(expiryDate, K, currencyPair,
                                        optionType, B,
                                        numObservationsPerYear,
                                        notional, notionalCurrency)

            value = option.value(valueDate, spotFXRate,
                                 domDiscountCurve, forDiscountCurve, model)

            start = time.time()
            modelParams = (spotFXRate, drift, volatility, scheme)
            valueMC = option.valueMC(valueDate,
                                     spotFXRate,
                                     domInterestRate,
                                     processType,
                                     modelParams)

            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value

            print(optionType, K, B, spotFXRate, value, valueMC,
                            diff, timeElapsed)

    end = time.time()

##########################################################################

    spotFXRates = range(50, 150, 10)
    B = 105.0

    print("Type", "K", "B", "S:", "Value", "Delta", "Vega", "Theta")

    for optionType in FinFXBarrierTypes:
        for spotFXRate in spotFXRates:
            barrierOption = FinFXBarrierOption(expiryDate,
                                               100.0,
                                               currencyPair,
                                               optionType,
                                               B,
                                               numObservationsPerYear,
                                               notional,
                                               notionalCurrency)

            value = barrierOption.value(valueDate,
                                        spotFXRate,
                                        domDiscountCurve,
                                        forDiscountCurve,
                                        model)

            delta = barrierOption.delta(valueDate,
                                        spotFXRate,
                                        domDiscountCurve,
                                        forDiscountCurve,
                                        model)

            vega = barrierOption.vega(valueDate,
                                      spotFXRate,
                                      domDiscountCurve,
                                      forDiscountCurve,
                                      model)

            theta = barrierOption.theta(valueDate,
                                        spotFXRate,
                                        domDiscountCurve,
                                        forDiscountCurve,
                                        model)

            print(optionType,
                            K,
                            B,
                            spotFXRate,
                            value,
                            delta,
                            vega,
                            theta)


test_FinFXBarrierOption()

