import sys
from tkinter import Widget
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget
from PyQt5 import QtCore as qtc
import psycopg2
import psycopg2.extras as extras
from config import config

# Global Variables
global_v_id = ''


class welcome_screen(QDialog):
    def __init__(self):
        super(welcome_screen, self).__init__()
        loadUi("welcome_screen.ui", self)
        self.cust_Button.clicked.connect(self.customer)
        self.station_Button.clicked.connect(self.station)
        self.register_Button.clicked.connect(self.register)

    def customer(self):
        Cportal = Customer_portal_screen()
        Widget.addWidget(Cportal)
        Widget.setCurrentIndex(Widget.currentIndex()+1)

    def station(self):
        Sportal = Station_portal_screen()
        Widget.addWidget(Sportal)
        Widget.setCurrentIndex(Widget.currentIndex()+1)

    def register(self):
        rportal = Register_portal_screen()
        Widget.addWidget(rportal)
        Widget.setCurrentIndex(Widget.currentIndex()+1)


class Register_portal_screen(QDialog):
    def __init__(self):
        super(Register_portal_screen, self).__init__()
        loadUi("Customer Registration.ui", self)
        self.button_reg.clicked.connect(self.details)
        self.home_button3.clicked.connect(self.home1)

    def details(self):
        vehicleNumber = str(self.lineEdit_ve.text())
        nic = str(self.lineEdit_ni.text())
        mobileNumber = str(self.lineEdit_nu.text())
        name = str(self.lineEdit_name.text())
        addr = str(self.lineEdit_ad.text())
        vehicleID = str(self.lineEdit_vid.text())
        fuel_t = str(self.box_ft.currentText())
        cust_t = str(self.box_gen.currentText())
        vehicle_t = str(self.box_vt.currentText())
        fuel_q = str(self.box_fq.currentText())
        print(vehicleNumber, vehicleID)
        conn = None
        try:
            if len(vehicleNumber) == 0 or len(nic) == 0 or len(mobileNumber) == 0 or len(name) == 0 or len(addr) == 0 or len(vehicleID) == 0:
                self.lbl_error_all.setText("Please Input All Fields.")

            elif len(vehicleNumber) != 8 and len(vehicleNumber) != 7:
                self.lbl_error_ve.setText("Check The vehicle number")

            elif len(vehicleID) != 13 and len(vehicleID) != 12:
                self.lbl_error_vid.setText("Check The User Id")

            elif len(mobileNumber) != 10:
                self.lbl_error_nu.setText("Number Should Contain 10 Digits")

            elif len(nic) != 10 and len(nic) != 12:
                self.lbl_error_ni.setText("Check The NIC ")
            else:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor(cursor_factory=extras.RealDictCursor)
                cur.execute(
                    f"INSERT INTO owner_details (v_id,cust_type,nic,name,address,phone_number) VALUES ('{vehicleID}','{cust_t}','{nic}','{name}','{addr}','{mobileNumber}')")
                cur.execute(
                    f"INSERT INTO vehicle_details (v_id,vehicle_number,vehicle_type,fuel_type,fuel_quality) VALUES ('{vehicleID}','{vehicleNumber}','{vehicle_t}','{fuel_t}','{fuel_q}')")
                #updated_rows = cur.rowcount
                # Commit the changes to the database
                conn.commit()
                cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def home1(self):
        h_ome = welcome_screen()
        Widget.addWidget(h_ome)
        Widget.setCurrentIndex(Widget.currentIndex()+1)


class Station_portal_screen(QDialog):
    def __init__(self):
        super(Station_portal_screen, self).__init__()
        loadUi("Fuel Availability.ui", self)
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor(cursor_factory=extras.RealDictCursor)
            cur.execute(f"SELECT * FROM fuel_availability")
            items = cur.fetchall()
            cur.close()
            data = {}
            for item in items:
                data[item["fuel_type"]] = item["fuel_remaining"]
            self.lcd92.display(data["p92"])
            self.lcd95.display(data["p95"])
            self.lcdauto.display(data["dauto"])
            self.lcdsuper.display(data["dsuper"])
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        self.edit_Button.clicked.connect(self.edit1)
        self.h1button.clicked.connect(self.home1)

    def edit1(self):
        e_dit = edit_screen()
        Widget.addWidget(e_dit)
        Widget.setCurrentIndex(Widget.currentIndex()+1)

    def home1(self):
        h_ome = welcome_screen()
        Widget.addWidget(h_ome)
        Widget.setCurrentIndex(Widget.currentIndex()+1)


class edit_screen(QDialog):
    def __init__(self):
        super(edit_screen, self).__init__()
        loadUi("Update Stock.ui", self)
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor(cursor_factory=extras.RealDictCursor)
            cur.execute(f"SELECT * FROM fuel_availability")
            items = cur.fetchall()
            cur.close()
            data = {}
            for item in items:
                data[item["fuel_type"]] = item["fuel_stoke"]
            self.lineEdit_2.setText(str(data["p92"]))
            self.lineEdit_4.setText(str(data["p95"]))
            self.lineEdit_3.setText(str(data["dauto"]))
            self.lineEdit.setText(str(data["dsuper"]))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        self.save1_Button.clicked.connect(self.stock)

    def stock(self):

        p92 = float(self.lineEdit_2.text())
        p95 = float(self.lineEdit_4.text())
        dauto = float(self.lineEdit_3.text())
        dsuper = float(self.lineEdit.text())
        conn = None

        new_fuel = {}
        new_fuel["p92"] = p92
        new_fuel["p95"] = p95
        new_fuel["dauto"] = dauto
        new_fuel["dsuper"] = dsuper
        print("test")
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor(cursor_factory=extras.RealDictCursor)
            cur.execute(
                f"UPDATE fuel_availability SET fuel_stoke='{p92}' WHERE fuel_type='p92'")
            cur.execute(
                f"UPDATE fuel_availability SET fuel_stoke='{p95}' WHERE fuel_type='p95'")
            cur.execute(
                f"UPDATE fuel_availability SET fuel_stoke='{dauto}' WHERE fuel_type='dauto'")
            cur.execute(
                f"UPDATE fuel_availability SET fuel_stoke='{dsuper}' WHERE fuel_type='dsuper'")

            query_fuel_availability = f"SELECT * FROM fuel_availability"
            cur.execute(query_fuel_availability)
            fuel_all = cur.fetchall()

            for f in fuel_all:
                print(f['fuel_type'])
                cur.execute(
                    f"UPDATE fuel_availability SET fuel_remaining='{f['fuel_remaining']+new_fuel[f['fuel_type']]}' WHERE fuel_type='{f['fuel_type']}'")

            updated_rows = cur.rowcount
            # Commit the changes to the database
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        s_tock = Station_portal_screen()
        Widget.addWidget(s_tock)
        Widget.setCurrentIndex(Widget.currentIndex()+1)


class Customer_portal_screen(QDialog):
    def __init__(self):
        super(Customer_portal_screen, self).__init__()
        loadUi("Customer portal.ui", self)
        self.enter_Button.clicked.connect(self.weekly_Quota)
        self.h2_button.clicked.connect(self.home1)

    def home1(self):
        h_ome = welcome_screen()
        Widget.addWidget(h_ome)
        Widget.setCurrentIndex(Widget.currentIndex()+1)

    def weekly_Quota(self):
        self.v_id = self.lineEdit_id.text()
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            query = f"SELECT EXISTS(SELECT 1 FROM owner_details WHERE v_id='{self.v_id}')"
            cur.execute(query)
            exist = cur.fetchone()
            exist = exist[0]
            cur.close()
            if exist:
                print("Sucsusfully loged in")

                W_quota = quota_screen(self.v_id)
                Widget.addWidget(W_quota)
                Widget.setCurrentIndex(Widget.currentIndex()+1)
            elif len(self.v_id) == 0:
                self.label_error.setText("Please Input All Fields.")
            else:
                self.label_error.setText("Please Insert Correct Vehicle Id.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


class quota_screen(QDialog):
    def __init__(self, v_id):
        super(quota_screen, self).__init__()
        loadUi("weekly_Allow.ui", self)
        self.next_Button.clicked.connect(self.customer)
        self.new_button.clicked.connect(self.next)
        self.remaining = 0
        conn = None
        self.v_id = v_id
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            query = f"SELECT fuel_remaining FROM vehicle_details WHERE v_id='{self.v_id}'"
            cur.execute(query)
            self.remaining = cur.fetchone()
            self.remaining = float(self.remaining[0])
            self.lcdsuper.display(self.remaining)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def customer(self):
        pumped = float(self.line_amount.text())
        new_remainder = self.remaining - pumped
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            fuel_key = self.v_id[-3:-1]
            if fuel_key == "ND":
                fuel_type = "dauto"
            elif fuel_key == "SD":
                fuel_type = "dsuper"
            elif fuel_key == "NP":
                fuel_type = "p92"
            else:
                fuel_type = "p95"

            query_get_fuel = f"SELECT * FROM fuel_availability WHERE fuel_type = '{fuel_type}'"
            cur.execute(query_get_fuel)
            get_fuel_result = cur.fetchone()

            current_stock = float(get_fuel_result[2])
            station_remaning = current_stock - pumped

            query_update_stoke = f"UPDATE fuel_availability SET fuel_remaining='{station_remaning}' WHERE fuel_type = '{fuel_type}'"
            cur.execute(query_update_stoke)

            query = f"UPDATE vehicle_details SET fuel_remaining='{new_remainder}' WHERE v_id='{self.v_id}'"
            cur.execute(query)

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        # print(pumped, new_remainder)

    def next(self):
        Cportal = Customer_portal_screen()
        Widget.addWidget(Cportal)
        Widget.setCurrentIndex(Widget.currentIndex()+1)


# main
app = QApplication(sys.argv)
welcome = welcome_screen()
Widget = QStackedWidget()
Widget.addWidget(welcome)
Widget.setFixedHeight(600)
Widget.setFixedWidth(800)
Widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exting")
