"""
    json格式转sqlalchemy对象
"""
from model.models import AccBaseInfo, AccBalance, AccTraded


# 参数为result['data']中的json列表和模型类型, 如：账号模型，余额模型或流水模型
def dict_to_obj(model_type, json_list):
    acc_obj_list = []
    # 账号模型
    if model_type == "acc_info":
        for json_data in json_list:
            acc_obj = AccBaseInfo()
            # 判断json数据是否含有对应keys
            if "bank_type" in json_data.keys():
                acc_obj.bank_type = json_data["bank_type"]
            if "acc_number" in json_data.keys():
                acc_obj.acc_number = json_data["acc_number"]
            if "acc_name" in json_data.keys():
                acc_obj.acc_name = json_data["acc_name"]
            if "acc_status" in json_data.keys():
                acc_obj.acc_status = json_data["acc_status"]
            if "acc_type" in json_data.keys():
                acc_obj.acc_type = json_data["acc_type"]
            if "acc_info" in json_data.keys():
                acc_obj.acc_info = json_data["acc_info"]
            if "acc_open_bank_name" in json_data.keys():
                acc_obj.acc_open_bank_name = json_data["acc_open_bank_name"]
            if "acc_author" in json_data.keys():
                acc_obj.acc_author = json_data["acc_author"]
            if "acc_id" in json_data.keys():
                acc_obj.acc_id = json_data["acc_id"]
            if "combination_name" in json_data.keys():
                acc_obj.combination_name = json_data["combination_name"]
            if "project_id" in json_data.keys():
                acc_obj.project_id = json_data["project_id"]
            if "createdAt" in json_data.keys():
                acc_obj.created_at = json_data["createdAt"]
            if "updatedAt" in json_data.keys():
                acc_obj.updated_at = json_data["updatedAt"]
            if "deletedAt" in json_data.keys():
                acc_obj.deleted_at = json_data["deletedAt"]
            if "endAt" in json_data.keys():
                acc_obj.end_at = json_data["endAt"]
            acc_obj_list.append(acc_obj)

    # 余额模型
    if model_type == "acc_balance":
        for json_data in json_list:
            acc_obj = AccBalance()
            # 判断json数据是否含有对应keys
            if "bank_type" in json_data.keys():
                acc_obj.bank_type = json_data["bank_type"]
            if "acc_number" in json_data.keys():
                acc_obj.acc_number = json_data["acc_number"]
            if "acc_name" in json_data.keys():
                acc_obj.acc_name = json_data["acc_name"]
            if "acc_type" in json_data.keys():
                acc_obj.acc_type = json_data["acc_type"]
            if "acc_currency" in json_data.keys():
                acc_obj.acc_currency = json_data["acc_currency"]
            if "acc_balance" in json_data.keys():
                acc_obj.acc_balance = json_data["acc_balance"]
            if "acc_freeze_balance" in json_data.keys():
                acc_obj.acc_freeze_balance = json_data["acc_freeze_balance"]
            if "acc_available_balance" in json_data.keys():
                acc_obj.acc_available_balance = json_data["acc_available_balance"]
            if "acc_open_bank_name" in json_data.keys():
                acc_obj.acc_open_bank_name = json_data["acc_open_bank_name"]
            if "acc_begin_date" in json_data.keys():
                acc_obj.acc_begin_date = json_data["acc_begin_date"]
            if "acc_status" in json_data.keys():
                acc_obj.acc_status = json_data["acc_status"]
            if "acc_control_status" in json_data.keys():
                acc_obj.acc_control_status = json_data["acc_control_status"]
            if "acc_book_balance" in json_data.keys():
                acc_obj.acc_book_balance = json_data["acc_book_balance"]
            if "acc_okay_bye" in json_data.keys():
                acc_obj.acc_okay_bye = json_data["acc_okay_bye"]
            if "acc_daily_balance" in json_data.keys():
                acc_obj.acc_daily_balance = json_data["acc_daily_balance"]
            if "deposit_type" in json_data.keys():
                acc_obj.deposit_type = json_data["deposit_type"]
            if "acc_id" in json_data.keys():
                acc_obj.acc_id = json_data["acc_id"]
            if "acc_interestrate" in json_data.keys():
                acc_obj.acc_interestrate = json_data["acc_interestrate"]
            if "currency_type_code" in json_data.keys():
                acc_obj.currency_type_code = json_data["currency_type_code"]
            if "account_state_code" in json_data.keys():
                acc_obj.account_state_code = json_data["account_state_code"]
            if "combination_name" in json_data.keys():
                acc_obj.combination_name = json_data["combination_name"]
            if "interestrate_model" in json_data.keys():
                acc_obj.interestrate_model = json_data["interestrate_model"]
            if "interestrate_project" in json_data.keys():
                acc_obj.interestrate_project = json_data["interestrate_project"]
            if "agreement_base" in json_data.keys():
                acc_obj.agreement_base = json_data["agreement_base"]
            if "acc_balance_date" in json_data.keys():
                acc_obj.acc_balance_date = json_data["acc_balance_date"]
            if "acc_income" in json_data.keys():
                acc_obj.acc_income = json_data["acc_income"]
            if "acc_expenditure" in json_data.keys():
                acc_obj.acc_expenditure = json_data["acc_expenditure"]
            if "batch_id" in json_data.keys():
                acc_obj.batch_id = json_data["batch_id"]
            if "createdAt" in json_data.keys():
                acc_obj.created_at = json_data["createdAt"]
            if "updatedAt" in json_data.keys():
                acc_obj.updated_at = json_data["updatedAt"]
            if "deletedAt" in json_data.keys():
                acc_obj.deleted_at = json_data["deletedAt"]
            acc_obj_list.append(acc_obj)

    # 流水模型
    if model_type == "acc_traded":
        for json_data in json_list:
            acc_obj = AccTraded()
            # 判断json数据是否含有对应keys
            if "bank_type" in json_data.keys():
                acc_obj.bank_type = json_data["bank_type"]
            if "acc_number" in json_data.keys():
                acc_obj.acc_number = json_data["acc_number"]
            if "acc_transaction_date" in json_data.keys():
                acc_obj.acc_transaction_date = json_data["acc_transaction_date"]
            if "acc_transaction_type" in json_data.keys():
                acc_obj.acc_transaction_type = json_data["acc_transaction_type"]
            if "acc_business_type" in json_data.keys():
                acc_obj.acc_business_type = json_data["acc_business_type"]
            if "acc_currency" in json_data.keys():
                acc_obj.acc_currency = json_data["acc_currency"]
            if "acc_voucher_number" in json_data.keys():
                acc_obj.acc_voucher_number = json_data["acc_voucher_number"]
            if "acc_revenue_expenditure" in json_data.keys():
                acc_obj.acc_revenue_expenditure = json_data["acc_revenue_expenditure"]
            if "acc_drawee_money" in json_data.keys():
                acc_obj.acc_drawee_money = json_data["acc_drawee_money"]
            if "acc_credit_money" in json_data.keys():
                acc_obj.acc_credit_money = json_data["acc_credit_money"]
            if "acc_balance" in json_data.keys():
                acc_obj.acc_balance = json_data["acc_balance"]
            if "acc_opposite_number" in json_data.keys():
                acc_obj.acc_opposite_number = json_data["acc_opposite_number"]
            if "acc_opposite_name" in json_data.keys():
                acc_obj.acc_opposite_name = json_data["acc_opposite_name"]
            if "acc_opposite_open_name" in json_data.keys():
                acc_obj.acc_opposite_open_name = json_data["acc_opposite_open_name"]
            if "acc_abstract" in json_data.keys():
                acc_obj.acc_abstract = json_data["acc_abstract"]
            if "acc_remarks" in json_data.keys():
                acc_obj.acc_remarks = json_data["acc_remarks"]
            if "acc_pay_use" in json_data.keys():
                acc_obj.acc_pay_use = json_data["acc_pay_use"]
            if "acc_drawee_line_no" in json_data.keys():
                acc_obj.acc_drawee_line_no = json_data["acc_drawee_line_no"]
            if "acc_payee_line_no" in json_data.keys():
                acc_obj.acc_payee_line_no = json_data["acc_payee_line_no"]
            if "acc_start_interest" in json_data.keys():
                acc_obj.acc_start_interest = json_data["acc_start_interest"]
            if "acc_exchange_rate" in json_data.keys():
                acc_obj.acc_exchange_rate = json_data["acc_exchange_rate"]
            if "acc_transaction_no" in json_data.keys():
                acc_obj.acc_transaction_no = json_data["acc_transaction_no"]
            if "acc_customer_no" in json_data.keys():
                acc_obj.acc_customer_no = json_data["acc_customer_no"]
            if "acc_customer_number" in json_data.keys():
                acc_obj.acc_customer_number = json_data["acc_customer_number"]
            if "acc_record_identifier" in json_data.keys():
                acc_obj.acc_record_identifier = json_data["acc_record_identifier"]
            if "acc_create_date" in json_data.keys():
                acc_obj.acc_create_date = json_data["acc_create_date"]
            if "acc_daily_balance" in json_data.keys():
                acc_obj.acc_daily_balance = json_data["acc_daily_balance"]
            if "acc_voucher_number" in json_data.keys():
                acc_obj.acc_voucher_number = json_data["acc_voucher_number"]
            if "acc_traded_code" in json_data.keys():
                acc_obj.cmb_acc_traded_code = json_data["acc_traded_code"]
            if "acc_author" in json_data.keys():
                acc_obj.acc_author = json_data["acc_author"]
            if "acc_summary" in json_data.keys():
                acc_obj.acc_summary = json_data["acc_summary"]
            if "acc_summary" in json_data.keys():
                acc_obj.acc_summary = json_data["acc_summary"]
            if "cr_currency_type_code" in json_data.keys():
                acc_obj.currency_type_code = json_data["currency_type_code"]
            if "account_state_code" in json_data.keys():
                acc_obj.account_state_code = json_data["account_state_code"]
            if "acc_tran_desc" in json_data.keys():
                acc_obj.acc_tran_desc = json_data["acc_tran_desc"]
            if "acc_charge_fee" in json_data.keys():
                acc_obj.acc_charge_fee = json_data["acc_charge_fee"]
            if "account_type_show" in json_data.keys():
                acc_obj.account_type_show = json_data["account_type_show"]
            if "acc_end_interest" in json_data.keys():
                acc_obj.acc_end_interest = json_data["acc_end_interest"]
            if "acc_id" in json_data.keys():
                acc_obj.acc_id = json_data["acc_id"]
            if "batch_id" in json_data.keys():
                acc_obj.batch_id = json_data["batch_id"]
            if "createdAt" in json_data.keys():
                acc_obj.created_at = json_data["createdAt"]
            if "updatedAt" in json_data.keys():
                acc_obj.updated_at = json_data["updatedAt"]
            if "deletedAt" in json_data.keys():
                acc_obj.deleted_at = json_data["deletedAt"]
            if "login_user" in json_data.keys():
                acc_obj.login_user = json_data["login_user"]
            if "acc_bill_number" in json_data.keys():
                acc_obj.acc_bill_number = json_data["acc_bill_number"]
            if "verification_code" in json_data.keys():
                acc_obj.verification_code = json_data["verification_code"]
            if "instructions" in json_data.keys():
                acc_obj.instructions = json_data["instructions"]
            if "customer_number" in json_data.keys():
                acc_obj.customer_number = json_data["customer_number"]
            if "type_message" in json_data.keys():
                acc_obj.type_message = json_data["type_message"]
            if "business_identification_number" in json_data.keys():
                acc_obj.business_identification_number = json_data["business_identification_number"]
            if "launch_line_number" in json_data.keys():
                acc_obj.launch_line_number = json_data["launch_line_number"]
            if "launch_bank_name" in json_data.keys():
                acc_obj.launch_bank_name = json_data["launch_bank_name"]
            if "revenue_number" in json_data.keys():
                acc_obj.revenue_number = json_data["revenue_number"]
            if "receive_bank_number" in json_data.keys():
                acc_obj.receive_bank_number = json_data["receive_bank_number"]
            if "trade_agency" in json_data.keys():
                acc_obj.trade_agency = json_data["trade_agency"]
            if "trade_channel" in json_data.keys():
                acc_obj.trade_channel = json_data["trade_channel"]
            if "receipt_number" in json_data.keys():
                acc_obj.receipt_number = json_data["receipt_number"]
            if "handle" in json_data.keys():
                acc_obj.handle = json_data["handle"]
            if "account_network" in json_data.keys():
                acc_obj.account_network = json_data["account_network"]
            if "account_user" in json_data.keys():
                acc_obj.account_user = json_data["account_user"]
            if "payment_open_bank" in json_data.keys():
                acc_obj.payment_open_bank = json_data["payment_open_bank"]
            if "payment_account_number" in json_data.keys():
                acc_obj.payment_account_number = json_data["payment_account_number"]
            if "print_method" in json_data.keys():
                acc_obj.print_method = json_data["print_method"]
            if "network_number" in json_data.keys():
                acc_obj.network_number = json_data["network_number"]
            if "set_number" in json_data.keys():
                acc_obj.set_number = json_data["set_number"]
            if "area_number" in json_data.keys():
                acc_obj.area_number = json_data["area_number"]
            if "print_time" in json_data.keys():
                acc_obj.print_time = json_data["print_time"]
            if "print_count" in json_data.keys():
                acc_obj.print_count = json_data["print_count"]
            if "bank_note_mark" in json_data.keys():
                acc_obj.bank_note_mark = json_data["bank_note_mark"]
            if "trade_state" in json_data.keys():
                acc_obj.trade_state = json_data["trade_state"]
            if "receipt_production_time" in json_data.keys():
                acc_obj.receipt_production_time = json_data["receipt_production_time"]
            if "own_open_bank" in json_data.keys():
                acc_obj.own_open_bank = json_data["own_open_bank"]
            if "back_check_code" in json_data.keys():
                acc_obj.back_check_code = json_data["back_check_code"]

    # 返回对象
    return acc_obj_list
