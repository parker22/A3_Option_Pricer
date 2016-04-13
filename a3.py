# -*- coding: UTF-8 -*-
# Filename: Assignment2.py
# COMP7405 Assignment3
# Author: LIU Jiahe (3035237365) ZHAN Hui(xxxxxxxxxx)

import traceback
import sys, os
from math import *
from scipy.stats import norm
from PyQt5 import QtWidgets, QtGui
from option_ui import Ui_OptionPricer
from Utilities import black_scholes, binomial_tree, closed_form, implied_volatility, monte_carlo


class OptionUI(QtWidgets.QMainWindow, Ui_OptionPricer):
    def __init__(self):
        super(OptionUI, self).__init__()
        self.setupUi(self)

        # Quit Confirmation Dialog
        self.actionExit.triggered.connect(self.msg)  #
        self.widget_asian_pars.hide()
        self.lineEdit_step.setVisible(False)
        self.label_step.setVisible(False)
        self.lineEdit_path.setVisible(False)
        self.label_paths.setVisible(False)
        self.widget_asset2.hide()
        self.groupBox_control_variate.hide()
        self.comboBox_kindof_option.currentIndexChanged.connect(self.option_kind_changed)
        self.lineEdit_stock_price.setValidator(QtGui.QDoubleValidator())
        self.lineEdit_maturity.setValidator(QtGui.QDoubleValidator())
        self.lineEdit_path.setValidator(QtGui.QDoubleValidator())
        self.lineEdit_step.setValidator(QtGui.QDoubleValidator())
        self.lineEdit_strike_price.setValidator(QtGui.QDoubleValidator())
        self.lineEdit_vol1.setValidator(QtGui.QDoubleValidator())
        self.lineEdit_rate.setValidator(QtGui.QDoubleValidator())
        self.lineEdit_corr.setValidator(QtGui.QDoubleValidator())
        self.lineEdit_stock_price_2.setValidator(QtGui.QDoubleValidator())
        self.lineEdit_vol2.setValidator(QtGui.QDoubleValidator())
        self.pushButton_calculate.clicked.connect(self.calculate_result)
        self.init_method(False)
        self.radioButton_asset_single.toggled.connect(lambda: self.init_basket(False))
        self.radioButton_asset_basket.toggled.connect(lambda: self.init_basket(True))
        self.radioButton_type_geo.toggled.connect(lambda: self.init_method(False))
        self.radioButton_type_arith.toggled.connect(lambda: self.init_method(True))

    def init_basket(self, basket):
        if basket:
            self.widget_asset2.show()
            self.label_step.hide()
            self.lineEdit_step.hide()
        else:
            self.widget_asset2.hide()
            self.label_step.show()
            self.lineEdit_step.show()


    def init_method(self, method):
        if method:
            self.groupBox_control_variate.show()
            self.label_paths.show()
            self.lineEdit_path.show()
        else:
            self.groupBox_control_variate.hide()
            self.label_paths.hide()
            self.lineEdit_path.hide()


    def get_exercise(self):
        if self.comboBox_kindof_option.currentIndex() == 0:
            return 'EU'
        elif self.comboBox_kindof_option.currentIndex() == 1:
            return 'AM'
        elif self.comboBox_kindof_option.currentIndex() == 2:
            return 'AS'
        elif self.comboBox_kindof_option.currentIndex() == 3:
            return 'IV'

    def get_parameters(self):
        try:
            s = float(self.lineEdit_stock_price.text())
            k = float(self.lineEdit_strike_price.text())
            mat_t = float(self.lineEdit_maturity.text())
            r = float(self.lineEdit_rate.text()) / 100
            vol = float(self.lineEdit_vol1.text()) / 100
        except ValueError:

            return

        return s, k, mat_t, r, vol

    def get_addition_par(self, raw_obj):
        try:
            v = float(raw_obj.text())
            print "V= %s" % v
            return v

        except ValueError:
            return

    def show_error(self, message):
        q = QtWidgets.QErrorMessage()
        q.showMessage(str(message))
        q.exec_()

    def get_asian_pars(self):
        assets = None
        type = None
        cv = "STD"
        if self.radioButton_asset_basket.isChecked():
            assets = 2
        elif self.radioButton_asset_single.isChecked():
            assets = 1
        if self.radioButton_type_arith.isChecked():
            type = 'ARI'
        elif self.radioButton_type_geo.isChecked():
            type = 'GEO'
        if self.radioButton_cv_standard.isChecked():
            cv = "STD"
        elif self.radioButton_cv_geo.isChecked():
            cv = "GEO"

        return assets, type, cv

    def get_option_type(self):
        if self.radioButton_call.isChecked():
            return "%s_C" % self.get_exercise()
        elif self.radioButton_put.isChecked():
            return "%s_P" % self.get_exercise()
        else:

            # call error here
            return

    def calculate_result(self):

        try:
            s, k, mat_t, r, vol = self.get_parameters()
            option_type = self.get_option_type()

            if option_type == 'EU_C':
                print option_type
                result = black_scholes.c_price(s, k, mat_t, vol, r, 0)

            elif option_type == 'EU_P':
                print option_type
                result = black_scholes.p_price(s, k, mat_t, vol, r, 0)

            elif option_type == 'AM_C':
                print option_type
                n = self.get_addition_par(self.lineEdit_step)
                result = binomial_tree.binomial_option('C', mat_t, s, k, r, vol, int(n))

            elif option_type == 'AM_P':
                n = self.get_addition_par(self.lineEdit_step)
                print option_type
                result = binomial_tree.binomial_option('P', mat_t, s, k, r, vol, int(n))

            elif option_type == 'IV_C':
                print option_type
                p = self.get_addition_par(self.lineEdit_step)
                result = implied_volatility.implied_volatility('C', s, k, mat_t, r, p, vol)

            elif option_type == 'IV_P':
                p = self.get_addition_par(self.lineEdit_step)
                print option_type
                result = implied_volatility.implied_volatility('P', s, k, mat_t, r, p, vol)
            elif option_type == 'AS_C':
                print option_type
                assets, type, cv = self.get_asian_pars()
                if assets == 1:
                    if type == 'GEO':
                        n = self.get_addition_par(self.lineEdit_step)
                        result = closed_form.geo_asian('C', s, k, mat_t, r, vol, n)
                    if type == 'ARI':
                        n = self.get_addition_par(self.lineEdit_step)
                        m = self.get_addition_par(self.lineEdit_path)
                        result = monte_carlo.ari_asian('C', s, k, mat_t, r, vol, int(n), int(m), cv)[0]
                if assets == 2:
                    if type == 'GEO':
                        s2 = self.get_addition_par(self.lineEdit_stock_price_2)
                        v2 = self.get_addition_par(self.lineEdit_vol2)/100
                        rho = self.get_addition_par(self.lineEdit_corr)/100
                        result = closed_form.geo_basket('C', s,s2, k,mat_t,r, vol,v2, rho)
                    if type == 'ARI':
                        s2 = self.get_addition_par(self.lineEdit_stock_price_2)
                        m = self.get_addition_par(self.lineEdit_path)
                        v2 = self.get_addition_par(self.lineEdit_vol2) / 100
                        rho = self.get_addition_par(self.lineEdit_corr) / 100
                        result = monte_carlo.ari_basket('C', s, s2, k ,mat_t, r, vol, v2, rho, int(m), cv)[0]

            elif option_type == 'AS_P':
                print option_type
                assets, type, cv = self.get_asian_pars()
                if assets == 1:
                    if type == 'GEO':
                        n = self.get_addition_par(self.lineEdit_step)
                        result = closed_form.geo_asian('P', s, k, mat_t, r, vol, n)
                    if type == 'ARI':
                        n = self.get_addition_par(self.lineEdit_step)
                        m = self.get_addition_par(self.lineEdit_path)
                        result = monte_carlo.ari_asian('P', s, k, mat_t, r, vol, int(n), int(m), cv)[0]
                if assets == 2:
                    if type == 'GEO':
                        s2 = self.get_addition_par(self.lineEdit_stock_price_2)
                        v2 = self.get_addition_par(self.lineEdit_vol2) / 100
                        rho = self.get_addition_par(self.lineEdit_corr) / 100
                        result = closed_form.geo_basket('P', s, s2, k, mat_t, r, vol, v2, rho)
                    if type == 'ARI':
                        s2 = self.get_addition_par(self.lineEdit_stock_price_2)
                        m = self.get_addition_par(self.lineEdit_path)
                        v2 = self.get_addition_par(self.lineEdit_vol2) / 100
                        rho = self.get_addition_par(self.lineEdit_corr) / 100
                        result = monte_carlo.ari_basket('P', s, s2, k, mat_t, r, vol, v2, rho, int(m), cv)[0]

            self.label_result_value.setText(str(result))
            print result

        except TypeError:
            self.show_error("Please input all parameters ....")
            print "Error"

    def msg(self):
        reply = QtWidgets.QMessageBox.question(self,
                                               "Exit",
                                               "Are you sure?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            print "Yes"
            Ui_OptionPricer.close()

    def option_kind_changed(self, i):
        if i == 0:  # European
            self.widget_asset2.hide()
            self.widget_asian_pars.hide()
            self.lineEdit_step.setVisible(False)
            self.label_step.setVisible(False)
            self.lineEdit_path.setVisible(False)
            self.label_paths.setVisible(False)
            self.label_vol1.setText("Volatility: (%)")
            pass
        elif i == 1:  # American
            self.widget_asset2.hide()
            self.widget_asian_pars.hide()
            self.lineEdit_step.setVisible(True)
            self.label_step.setVisible(True)
            self.lineEdit_path.setVisible(False)
            self.label_paths.setVisible(False)
            self.label_step.setText("Step:")
            self.label_vol1.setText("Volatility: (%)")

            pass
        elif i == 2:  # Asian
            # self.widget_asset2.show()
            self.widget_asian_pars.show()
            self.lineEdit_step.setVisible(True)
            self.label_step.setVisible(True)
            self.label_step.setText("Points:")
            self.label_vol1.setText("Volatility: (%)")

        elif i == 3:  # Implied Volatility
            self.widget_asset2.hide()
            self.widget_asian_pars.hide()
            self.lineEdit_step.setVisible(True)
            self.label_step.setVisible(True)
            self.lineEdit_path.setVisible(False)
            self.label_paths.setVisible(False)
            self.label_step.setText("Premium: ($)")
            self.label_vol1.setText("Repo Rate: (%)")


def bs_norm(d):
    return norm.cdf(d, 0, 1)


def geo_asian_option():
    s0 = 100
    sigma = 0.3
    r = 0.05
    mat_t = 3
    k = 100
    n = 50

    sigma_sq = pow(sigma, 2) * (n + 1) * (2 * n + 1) / (6 * n * n)
    mu = 0.5 * sigma_sq + (r - 0.5 * pow(sigma, 2)) * (n + 1) / (2 * n)
    d1 = (log(s0 / k) + (mu + 0.5 * pow(sigma_sq, 2)) * mat_t) / (sqrt(sigma_sq * mat_t))
    d2 = d1 - sqrt(sigma_sq * mat_t)
    n1 = bs_norm(d1)
    n2 = bs_norm(d2)
    geo = exp(-r * mat_t) * (s0 * exp(mu * mat_t) * n1 - k * n2)

    print geo

    print "test"


def main():
    try:
        geo_asian_option()

        app = QtWidgets.QApplication(sys.argv)
        option_ui = OptionUI()
        option_ui.show()
        sys.exit(app.exec_())

    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
    except Exception:
        traceback.print_exc(file=sys.stdout)


if __name__ == "__main__":
    main()
