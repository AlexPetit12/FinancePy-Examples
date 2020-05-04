# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 21:52:16 2019

@author: Dominic O'Kane
"""
from financepy.products.credit.FinCDS import FinCDS
from financepy.finutils.FinMath import ONE_MILLION
from financepy.products.libor.FinLiborSwap import FinLiborSwap
from financepy.market.curves.FinLiborCurve import FinLiborCurve
from financepy.market.curves.FinCDSCurve import FinCDSCurve
from financepy.finutils.FinFrequency import FinFrequencyTypes
from financepy.finutils.FinDayCount import FinDayCountTypes
from financepy.finutils.FinDate import FinDate


##########################################################################
# TO DO
##########################################################################

##########################################################################


def buildLiborCurve(tradeDate):

    valuationDate = tradeDate.addDays(1)
    dcType = FinDayCountTypes.ACT_360
    depos = []

    depos = []
    fras = []
    swaps = []

    dcType = FinDayCountTypes.THIRTY_E_360_ISDA
    fixedFreq = FinFrequencyTypes.SEMI_ANNUAL
    settlementDate = valuationDate

    maturityDate = settlementDate.addMonths(12)
    swap1 = FinLiborSwap(
        settlementDate,
        maturityDate,
        0.0502,
        fixedFreq,
        dcType)
    swaps.append(swap1)

    maturityDate = settlementDate.addMonths(24)
    swap2 = FinLiborSwap(
        settlementDate,
        maturityDate,
        0.0502,
        fixedFreq,
        dcType)
    swaps.append(swap2)

    maturityDate = settlementDate.addMonths(36)
    swap3 = FinLiborSwap(
        settlementDate,
        maturityDate,
        0.0501,
        fixedFreq,
        dcType)
    swaps.append(swap3)

    maturityDate = settlementDate.addMonths(48)
    swap4 = FinLiborSwap(
        settlementDate,
        maturityDate,
        0.0502,
        fixedFreq,
        dcType)
    swaps.append(swap4)

    maturityDate = settlementDate.addMonths(60)
    swap5 = FinLiborSwap(
        settlementDate,
        maturityDate,
        0.0501,
        fixedFreq,
        dcType)
    swaps.append(swap5)

    liborCurve = FinLiborCurve(
        "USD_LIBOR", settlementDate, depos, fras, swaps)

    return liborCurve

##########################################################################


def buildIssuerCurve(tradeDate, liborCurve):

    valuationDate = tradeDate.addDays(1)

    cdsMarketContracts = []

    cdsCoupon = 0.0048375
    maturityDate = FinDate(2010, 6, 29)
    cds = FinCDS(valuationDate, maturityDate, cdsCoupon)
    cdsMarketContracts.append(cds)

    recoveryRate = 0.40

    issuerCurve = FinCDSCurve(valuationDate,
                              cdsMarketContracts,
                              liborCurve,
                              recoveryRate)
    return issuerCurve

##########################################################################


def test_valueCDSIndex():

    # We treat an index as a CDS contract with a flat CDS curve
    tradeDate = FinDate(2006, 2, 7)
    liborCurve = buildLiborCurve(tradeDate)
    issuerCurve = buildIssuerCurve(tradeDate, liborCurve)
    stepInDate = tradeDate.addDays(1)
    valuationDate = stepInDate
    maturityDate = FinDate(2010, 6, 20)

    cdsRecovery = 0.40
    notional = 10.0 * ONE_MILLION
    longProtection = True
    indexCoupon = 0.004

    cdsIndexContract = FinCDS(stepInDate,
                              maturityDate,
                              indexCoupon,
                              notional,
                              longProtection)

#    cdsIndexContract.print(valuationDate)

    print("LABEL", "VALUE")

    spd = cdsIndexContract.parSpread(
        valuationDate, issuerCurve, cdsRecovery) * 10000.0
    print("PAR SPREAD", spd)

    v = cdsIndexContract.value(valuationDate, issuerCurve, cdsRecovery)
    print("FULL VALUE", v['full_pv'])
    print("CLEAN VALUE", v['clean_pv'])

    p = cdsIndexContract.cleanPrice(valuationDate, issuerCurve, cdsRecovery)
    print("CLEAN PRICE", p)

    accruedDays = cdsIndexContract.accruedDays()
    print("ACCRUED DAYS", accruedDays)

    accruedInterest = cdsIndexContract.accruedInterest()
    print("ACCRUED COUPON", accruedInterest)

    protPV = cdsIndexContract.protectionLegPV(
        valuationDate, issuerCurve, cdsRecovery)
    print("PROTECTION LEG PV", protPV)

    premPV = cdsIndexContract.premiumLegPV(
        valuationDate, issuerCurve, cdsRecovery)
    print("PREMIUM LEG PV", premPV)

    fullRPV01, cleanRPV01 = cdsIndexContract.riskyPV01(
        valuationDate, issuerCurve)
    print("FULL  RPV01", fullRPV01)
    print("CLEAN RPV01", cleanRPV01)

#    cdsIndexContract.printFlows(issuerCurve)

test_valueCDSIndex()
