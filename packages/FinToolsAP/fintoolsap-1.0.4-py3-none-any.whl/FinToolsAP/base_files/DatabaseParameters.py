# every table must have 'TABLE', 'VARS_DATA_TYPE', 'DEFAULT_ID', 'DEFAULT_DATE'

class Tables:

    WRDS_USERNAME = None

    # list of tables from WRDS to make local
    WRDS_TABLES = ['FF.FACTORS_DAILY',          # FamaFrench Factors daily (used for risk-free rate) 
                   'FF.FACTORS_MONTHLY',        # FamaFrench Factors monthly (used for risk-free rate)
                   'CRSP.CCMXPF_LINKTABLE',     # CCM link table used to merge CRSP and Compustat
                   'CRSP.MSEDELIST',            # CRSP monthly delist events
                   'CRSP.MSF',                  # CRSP monthly stock file
                   'CRSP.MSENAMES',             # CRSP monthly event file
                   'COMPA.FUNDA',               # Compustat annual observations
                   'COMPA.FUNDQ',               # Compustat quarterly observations    
                   'COMP.BANK_FUNDA',           # Compustat bank annual observations 
                   'COMP.BANK_FUNDQ',           # Compustat bank quarterly observations 
                   'MFL.MFLINK1',               # CRSP Mutual Fund Link Table
                   'MFL.MFLINK2',               # Thompson Reuters Mutual Fund Link Table
                   'CRSP.PORTNOMAP',            # Map CRSP fundnos to CRSP portnos
                   'WRDSAPPS.BONDRET',          # WRDS Corporate Bond Return Data
                   'WRDSAPPS.BONDCRSP_LINK']    # WRDS Corpotate Bond/CRSP Link Table

           
    # list of created tables
    CREATED_TABLES = ['MFLINKS',        # Combined MFLinks table (i.e. mflink1 & mflink2)
                      'COMP_A',         # Modified annual compustat      
                      'COMP_Q',         # Modified quarterly compustat
                      'CRSP_D',         # CRSP daily file
                      'CRSP_M',         # CRSP monthly file (i.e. merged CRSP.MSF, CRSP.MSENAMES, CRSP.MSEDELIST) 
                      'CCM',            # CRSP/Compustat merged file 
                      'MF_HOLDINGS',    # Mutual fund holding data for combined Thopmson Reuters and CRSP data sets
                      'MF_CHAR',        # Mutual Fund Portfolio price multiples
                      'CORPBOND']       # WRDS Corporate Bond data

    CSV_TABLES = ['CRSP_DSF',           # CRSP daily file read in from the .csv file in CSVtoSQL/
                  'TFN_S12MASTER',      # Thompson Reuters Refinitiv s12 Mutual Funds Holdings (CSVtoSQL/~.csv)
                  'TFN_F13MASTER',      # Thompson Reuters Refinitiv f13 Instituional Holdings (CSVtoSQL/~.csv)
                  'IBES',               # IBES forecasts
                  'CRSP_MF',            # CRSP mutual fund holdings data raw
                  'BTDS']               # TRACE enhanced corp bond data 
    
    # remove rows from tables that have missing information
    SQL_CLEANING = {'BTDS':          {'null_rows': ['bond_sym_id', 'company_symbol']},
                    'TFN_F13MASTER': {'null_rows': ['mgrno', 'shares', 'cusip']},
                    'TFN_S12MASTER': {'null_rows': ['fundno', 'shares', 'cusip']}, 
                    'IBES':          {'null_rows': ['actual', 'value', 'cusip'], 'upper_cols': ['curr']}, 
                    'CRSP_MF':       {'null_rows': ['permno', 'nbr_shares', 'cusip']},
                   }
    
class TRACE:

    class BTDS:

        # For variable descriptions see:
        # https://wrds-www.wharton.upenn.edu/pages/support/manuals-and-overviews/trace/documentation-files-trace-enhanced-data/
        
        TABLE = 'BTDS'

        VARS_DATA_TYPE = {'bond_sym_id': str, 'company_symbol': str, 'cusip_id': str,
                          'bloomberg_identifier': str, 'trd_exctn_dt': 'datetime64[ns]', 
                          'trd_exctn_tm': 'datetime64[ns]', 'trd_rpt_dt': 'datetime64[ns]',
                          'trd_rpt_tm': 'datetime64[ns]', 'rptd_pr': float, 
                          'entrd_vol_qt': float, 'yld_pt': float, 'yld_sign_cd': str,
                          'msg_seq_nb': str, 'trc_st': str, 'wis_fl': str, 'cmsn_trd': str,
                          'agu_qsr_id': str, 'asof_cd': str, 'days_to_sttl_ct': str, 
                          'sale_cndtn_cd': str, 'sale_cndtn2_cd': str, 'spcl_trd_fl': str, 
                          'cntra_mp_id': str, 'rpt_side_cd': str, 'scrty_type_cd': str, 
                          'buy_cmsn_rt': str, 'buy_cpcty_cd': str, 'sell_cmsn_rt': str, 
                          'sell_cpcty_cd': str, 'trdg_mkt_cd': str, 'dissem_fl': str, 
                          'orig_msg_seq_nb': str, 'sub_prdct': str, 'stlmnt_dt': 'datetime64[ns]', 
                          'trd_mod_3': str, 'trd_mod_4': str, 'rptg_party_type': str, 
                          'lckd_in_ind': str, 'ats_indicator': str, 'pr_trd_dt': 'datetime64[ns]', 
                          'first_trade_ctrl_date': 'datetime64[ns]', 'first_trade_ctrl_num': str}
        
        DEFAULT_VARS = ['cusip_id', 'company_symbol', 'trd_exctn_dt', 'sub_prdct', 'wis_fl', 
                        'yld_pt', 'pr_trd_dt', 'stlmnt_dt']

        DEFAULT_DATE = 'trd_exctn_dt'
        DEFAULT_ID = 'cusip_id'
        DEFAULT_SALE_CONDITION = ['@']
        DEFAULT_TRADING_MARKET = ['S1']

class IBES:

    TABLE = 'IBES'

    VARS_DATA_TYPE = {'oftic': str, 'ticker': str, 'cusip': str, 'cname': str,
                      'fpedats': 'datetime64[ns]', 'actdats': 'datetime64[ns]',
                      'acttims': 'datetime64[ns]', 'revdats': 'datetime64[ns]',
                      'revtims': 'datetime64[ns]', 'anndats': 'datetime64[ns]',
                      'anntims': 'datetime64[ns]', 'estimator': str, 'analys': str,
                      'value': float, 'usfirm': 'Int8', 'currfl': str, 
                      'curr': str, 'report_curr': str, 'pdf': str, 'actual': float,
                      'curr_act': str, 'anndats_act': 'datetime64[ns]',
                      'anntims_act': 'datetime64[ns]', 'actdats_act': 'datetime64[ns]',
                      'acttims_act': 'datetime64[ns]', 'fpi': str, 'measure': str}
    
    VALID_MEASURES = ['EPS', 'BPS', 'CPS', 'CPX', 'CSH', 'DPS', 'EBG', 'EBI', 'EBS', 'EBT',
                      'ENT', 'EPX', 'FFO', 'GPS', 'GRM', 'NAV', 'NDT', 'NET', 'OPR', 'PRE',
                      'ROA', 'ROE', 'SAL']
    
    DEFAULT_VARS = ['cusip', 'anndats', 'actdats', 'fpedats', 'analys', 'measure', 'value', 'actual']

    # valid forecast period indicators (fpi) 
    # See https://wrds-www.wharton.upenn.edu/pages/get-data/ibes-thomson-reuters/ibes-academic/detail-history/detail/ 
    # for details 
    VALID_FPI = ['1', '2', '3', '4', '5', 'E', 'F', 'G', 'H', 'I', 'U', 'X', '6', '7', '8',
                 '9', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'L', 'Y', 'A', 'B', 'C', 'D', 'J',
                 'K', 'Z', '0']
    
    DEFAULT_DATE = 'anndats'
    DEFAULT_ID = 'cusip'
    DEFAULT_CURR = 'USD'
    DEFAULT_USFIRM = 1
    DEFAULT_MEASURE = ['EPS', 'BPS']
    DEFAULT_FPI = ['0', '1', '2']

class WRDS:

    class CorpBond:

        TABLE = 'CORPBOND'

        DEFAULT_ID = 'cusip'
        DEFAULT_DATE = 'date'

        VARS_DATA_TYPE = {'date': 'datetime64[ns]',  'issue_id': 'Int32', 'cusip': str,
                          'bond_sym_id': str, 'bsym': str, 'isin': str, 'company_symbol': str, 
                          'bond_type': str, 'security_level': str, 'conv': 'Int32', 
                          'offering_date': 'datetime64[ns]', 'offering_price': float, 
                          'offering_amt': float, 'principal_amt': float, 'maturity': 'datetime64[ns]', 
                          'treasury_maturity': str, 'coupon': float, 'day_count_basis': str, 
                          'dated_date': 'datetime64[ns]', 'first_interest_date': 'datetime64[ns]', 
                          'last_interest_date': 'datetime64[ns]', 'ncoups': 'Int32', 't_date': 'datetime64[ns]', 
                          't_volume': float, 't_dvolume': float, 't_spread': float, 't_yld_pt': float, 
                          'yield': float, 'amount_outstanding': float, 'price_eom': float, 'price_ldm': float,
                          'price_l5m': float, 'gap': 'Int32', 'coupmonth': 'Int32', 'nextcoup': 'datetime64[ns]', 
                          'coupamt': float, 'coupacc': float, 'multicoups': 'Int32', 'ret_eom': float, 
                          'ret_ldm': float, 'ret_l5m': float, 'tmt': float, 'remcoups': 'Int32',
                          'duration': float, 'r_sp': str, 'r_mr': str, 'r_fr': str, 'n_sp': 'Int32', 
                          'n_mr': 'Int32', 'n_fr': 'Int32', 'rating_num': 'Int32', 'rating_cat': str, 
                          'rating_class': str, 'defaulted': str, 'default_date': 'datetime64[ns]', 
                          'default_type': str, 'reinstated': str, 'reinstated_date': 'datetime64[ns]', 
                          'permno': 'Int32', 'permco': 'Int32'}
        
        DEFAULT_VARS = ['date', 'cusip', 'permno', 'permco', 'company_symbol', 'bond_type', 'maturity', 'yield']

        ALL_VARS = True

    class CRSPBondMap:

        TABLE = 'CRSPBONDMAP'

        DEFAULT_ID = 'cusip'
        DEFAULT_DATE = 'link_startdt'

        VARS_DATA_TYPE = {'cusip': str, 'permco': 'Int32', 'permno': 'Int32', 
                          'trace_startdt': 'datetime64[ns]', 'trace_enddt': 'datetime64[ns]', 
                          'crsp_startdt': 'datetime64[ns]', 'crsp_enddt': 'datetime64[ns]', 
                          'link_startdt': 'datetime64[ns]', 'link_enddt': 'datetime64[ns]'}

        DEFAULT_VARS = ['cusip', 'permno', 'permco', 'link_startdt', 'link_enddt']

    class MFLinks:

        TABLE = 'MFLINKS'
        
        DEFAULT_VARS = ['wficn', 'fundno', 'crsp_fundno', 'rdate', 'assets', 'ioc']
    
        VARS_DATA_TYPE = {'wficn': 'Int32', 'fundno': 'Int32', 'fundno_id': 'Int32',
                          'fdate': 'datetime64[ns]', 'fundname': str, 'rdate': 'datetime64[ns]',
                          'mgrcoab': str, 'assets': float, 'num_holdings': float, 
                          'pct_crsp_holdings': float, 'ioc': 'Int8', 'prdate': 'datetime64[ns]', 
                          'country': str, 'crsp_fundno': 'Int32'}
        
        DEFAULT_ID = 'wficn'
        DEFAULT_DATE = 'rdate'
        ALL_VARS = True

    class CCMLinks:

        TABLE = 'CCMLINKS'
        DEFAULT_ID = 'gvkey'
        DEFAULT_DATE = 'linkdt'

        DEFAULT_VARS = ['gvkey', 'permno', 'permco', 'linktype', 'linkprim', 'linkdt']

        VARS_DATA_TYPE = {'gvkey': str, 'permno': 'Int32', 'permco': 'Int32', 'linktype': str, 'linkprim': str,
                          'linkdt': 'datetime64[ns]', 'linkenddt': 'datetime64[ns]'}
        ALL_VARS = False


class Factors:

    TABLE = 'FACTORS'

    DEFAULT_VARS = ['date', 'mkt_rf', 'smb3', 'hml']

    VARS_DATA_TYPE = {'date': 'datetime64[ns]', 'mkt': float, 'rf': float, 
                      'mkt_rf': float, 'smb3': float, 'smb5': float, 'hml': float, 
                      'rmw': float, 'cma': float, 'mom': float, 'st_rev': float, 
                      'lt_rev': float}
    
    DEFAULT_ID = None
    DEFAULT_DATE = 'date'
    ALL_VARS = True

class ThompsonRetuers:

    class InstitutionalHoldings:

        TABLE = 'TFN_F13MASTER'

        DEFAULT_VARS = ['mgrno', 'rdate', 'cusip', 'shares']

        VARS_DATA_TYPE = {'mgrno': 'Int32', 'mgrname': str, 'typecode': 'Int16', 'country': str, 
                          'prdate': 'datetime64[ns]', 'fdate': 'datetime64[ns]', 
                          'rdate': 'datetime64[ns]', 'cusip': str, 'stkname': str, 'ticker': str, 
                          'exchcd': str, 'stkcd': str, 'stkcdesc': str, 'indcode': float, 'shares': float, 
                          'no': 'Int32', 'shared': 'Int32', 'sole': 'Int32',
                          'change': float, 'prc': float, 'shrout1': float, 'shrout2': float}

        DEFAULT_ID = 'mgrno'
        DEFAULT_DATE = 'rdate'
        ALL_VARS = True

    class MutualFunds:

        TABLE = 'TFN_S12MASTER'

        DEFAULT_VARS = ['fundno', 'rdate', 'cusip', 'shares']

        VARS_DATA_TYPE = {'fundno': 'Int32', 'fundname': str, 'mgrcoab': str, 'country': str, 'ioc': 'Int8', 'assets': float, 
                          'prdate': 'datetime64[ns]', 'fdate': 'datetime64[ns]', 'rdate': 'datetime64[ns]', 'cusip': str, 'stkname': str, 'ticker': str, 
                          'exchcd': 'Int8', 'stkcd': 'Int8', 'stkcdesc': str, 'indcode': 'Int16', 'shares': float, 'change': float, 
                          'prc': float, 'shrout1': float, 'shrout2': float}

        DEFAULT_ID = 'fundno'
        DEFAULT_DATE = 'rdate'
        ALL_VARS = True

class MutualFundCharacteristics:

    TABLE = 'MF_CHAR'
    
    DEFAULT_VARS = ['wficn', 'date', 'dp', 'be', 'bm', 'ffbm', 'ep', 'ffep', 'cfp', 'ffcfp', 'inv', 
                    'op', 'pr2_12', 'pr1_1', 'pr13_60', 'beta', 'ac', 'nsi']
    
    VARS_DATA_TYPE = {'wficn': 'Int32', 'date': 'datetime64[ns]', 'dp': float, 
                      'be': float, 'bm': float, 'ffbm': float, 'ep': float, 
                      'ffep': float, 'cfp': float, 'ffcfp': float, 'inv': float, 'op': float, 
                      'pr2_12': float, 'pr1_1': float, 'pr13_60': float, 'beta': float, 
                      'ac': float, 'nsi': float, 'dp_ew': float, 
                      'be_ew': float, 'bm_ew': float, 'ffbm_ew': float, 'ep_ew': float, 
                      'ffep_ew': float, 'cfp_ew': float, 'ffcfp_ew': float, 'inv_ew': float, 'op_ew': float, 
                      'pr2_12_ew': float, 'pr1_1_ew': float, 'pr13_60_ew': float, 'beta_ew': float, 
                      'ac_ew': float, 'nsi_ew': float}

    
    DEFAULT_ID = 'wficn'
    DEFAULT_DATE = 'date'
    DEFAULT_STOCK_ID = 'cusip'
    ALL_VARS = True

class MutualFundHoldings:

    TABLE = 'MF_HOLDINGS'

    DEFAULT_VARS = ['wficn', 'date', 'cusip', 'shares']

    VARS_DATA_TYPE = {'wficn': 'Int32', 'date': 'datetime64[ns]', 'src': str,
                      'crsp_fundno': 'Int32', 'fundno': 'Int32', 'cusip': str, 
                      'shares': float}

    DEFAULT_DATE = 'date'
    DEFAULT_ID = 'wficn'
    ALL_VARS = True


class CRSP:

    class MutualFunds:

        TABLE = 'CRSP_MF'

        DEFAULT_VARS = ['crsp_portno', 'report_dt', 'nbr_shares', 'cusip']

        VARS_DATA_TYPE = {'crsp_portno': 'Int32', 'report_dt': 'datetime64[ns]', 'security_rank': 'Int32', 
                          'eff_dt': 'datetime64[ns]', 'percent_tna': float, 'nbr_shares': float,
                          'market_val': float, 'security_name': str, 'cusip': str, 'permno': 'Int32',
                          'permco': 'Int32', 'ticker': str, 'coupon': float, 'maturity_dt': 'datetime64[ns]'}

        DEFAULT_ID = 'crsp_portno'
        DEFAULT_DATE = 'report_dt'
        ALL_VARS = True

    class CRSPPortnoMap:

        TABLE = 'CRSP_PORTNOMAP'

        DEFAULT_VARS = ['crsp_portno', 'crsp_fundno', 'begdt', 'enddt']

        VARS_DATA_TYPE = {'crsp_fundno': 'Int32', 'crsp_portno': 'Int32', 'begdt': 'datetime64[ns]',
                          'enddt': 'datetime64[ns]', 'cusip8': str, 'crsp_cl_grp': 'Int32',
                          'fund_name': str, 'ticker': str, 'ncusip': str, 'first_offer_dt': 'datetime64[ns]',
                          'mgmt_name': str, 'mgmt_cd': str, 'mgr_name': str, 'mgr_dt': 'datetime64[ns]', 
                          'adv_name': str, 'open_to_inv': str, 'retail_fund': str, 'inst_fund': str, 
                          'm_fund': str, 'index_fund_flag': str, 'vau_fund': str, 'et_flag': str, 
                          'end_dt': 'datetime64[ns]', 'dead_flag': str, 'delist_cd': str, 
                          'merge_fundno': 'Int32'}
    
        DEFAULT_ID = 'crsp_portno'
        DEFAULT_DATE = 'begdt'
        ALL_VARS = True

    class CRSP_M:
        TABLE = 'CRSP_M'

        DEFAULT_VARS = ['date', 'permno', 'permco', 'cusip', 'ticker', 'shrcd', 
                        'exchcd', 'prc', 'shrout', 'adjret', 'adjretx', 'adjcumret', 
                        'adjcumretx', 'me', 'dp', 'vol', 'turn', 'dvol', 'bidask', 'beta',
                        'pr1_1', 'pr2_12', 'pr13_60']
        
        VARS_DATA_TYPE = {'date': 'datetime64[ns]', 'cusip': str, 'permno': 'Int32', 
                          'permco' : 'Int32', 'comnam': str, 'compno': 'Int32', 'ticker': str, 
                          'primexch': str, 'tsymbol': str, 'secstat': str, 'hsiccd': 'Int32', 
                          'naics': 'Int32', 'siccd': 'Int32', 'trdstat': str, 'ncusip': str, 
                          'shrcd': 'Int32', 'exchcd': "Int32", 'issuno': 'Int32', 'hexcd': 'Int32', 
                          'shrcls': str,  'ret': float, 'retx': float, 'shrout': float, 
                          'prc': float, 'cfacshr': float, 'cfacpr': float,  'bidlo': float, 'bid': float, 
                          'ask': float, 'askhi': float, 'spread': float, 'altprc': float, 'vol': float, 
                          'dlstdt': 'datetime64[ns]', 'dlstcd': 'Int32', 'nwperm': 'Int32', 
                          'nwcomp': 'Int32', 'nextdt': 'datetime64[ns]', 'dlamt': float, 'dlretx': float, 
                          'dlprc': float, 'dlpdt': 'datetime64[ns]', 'dlret': float, 'acperm': 'Int32', 
                          'accomp': 'Int32', 'me': float, 'adjret': float, 'adjretx': float, 
                          'dvd': float, 'adjdvd': float, 'dp': float, 'openprc': float, 'numtrd': float, 
                          'cumret': float, 'cumretx': float, 'adjcumret': float, 'adjcumretx': float, 
                          'dvol': float,'turn': float, 'pr1_1': float, 'pr2_12': float, 'pr13_60': float, 
                          'prx1_1': float, 'prx2_12': float, 'prx13_60': float, 'nameendt': 'datetime64[ns]', 
                          'bidask': float, 'mkt': float, 'cov': float, 'var': float, 'beta': float}
        
        DEFAULT_ID = 'permco'
        DEFAULT_DATE = 'date'
        DEFAULT_EXCHCD = [1, 2, 3]   # NYSE, NYSE MKT, NASDAQ
        DEFAULT_SHRCD = [10, 11]   # US Common Stock
        ALL_VARS = True

    class CRSP_D:
        TABLE = 'CRSP_D'
    
        DEFAULT_VARS = ['date', 'permno', 'permco', 'cusip', 'ticker', 'shrcd', 
                          'exchcd', 'prc', 'shrout', 'adjret', 'adjretx', 'adjcumret', 
                          'adjcumretx', 'me', 'dp', 'vol']
    
    
        VARS_DATA_TYPE = {'date': 'datetime64[ns]', 'cusip': str, 'permno': 'Int32', 
                          'permco' : 'Int32', 'comnam': str, 'ticker': str, 
                          'primexch': str, 'tsymbol': str, 'secstat': str, 'hsiccd': 'Int32', 
                          'naics': 'Int32', 'siccd': 'Int32', 'trdstat': str, 'ncusip': str, 
                          'shrcd': 'Int32', 'exchcd': "Int32", 'issuno': 'Int32', 'hexcd': 'Int32', 
                          'shrcls': str,  'ret': float, 'retx': float, 'shrout': float, 
                          'prc': float, 'cfacshr': float, 'cfacpr': float,  'bidlo': float, 'bid': float, 
                          'ask': float, 'askhi': float, 'vol': float, 'dlstcd': 'Int32', 'nwperm': 'Int32', 
                          'nextdt': 'datetime64[ns]', 'dlamt': float, 'dlretx': float, 
                          'dlprc': float, 'dlpdt': 'datetime64[ns]', 'dlret': float, 'acperm': 'Int32', 
                          'accomp': 'Int32', 'me': float, 'adjret': float, 'adjretx': float, 
                          'dvd': float, 'adjdvd': float, 'dp': float, 'openprc': float, 'numtrd': float, 
                          'cumret': float, 'cumretx': float, 'adjcumret': float, 'adjcumretx': float, 
                          'dvol': float, 'turn': float, 'hsicig': 'Int32', 'hsicmg': 'Int32', 'nameendt': 'datetime64[ns]', 
                          'shrflg': 'Int32', 'shrenddt': 'datetime64[ns]', 'distcd': 'Int32', 'divamt': float,
                          'dclrdt': 'datetime64[ns]', 'rcrdt': 'datetime64[ns]', 'paydt': 'datetime64[ns]', 
                          'trtscd': 'Int32', 'nmsind': 'Int32', 'mmcnt': 'Int32', 'nsdinx': 'Int32', 'vwretd': float,
                          'vwretx': float, 'ewretd': float, 'ewretx': float, 'sprtrn': float, 'bidask': float}
    
        DEFAULT_ID = 'permco'
        DEFAULT_DATE = 'date'
        DEFAULT_EXCHCD = [1, 2, 3]   # NYSE, NYSE MKT, NASDAQ
        DEFAULT_SHRCD = [10, 11]   # US Common Stock
        ALL_VARS = True

class Compustat:

    class COMP_A:

        TABLE = 'COMP_A'

        DEFAULT_VARS = ['gvkey', 'datadate', 'tic', 'at', 'sale', 'cogs', 'act', 'txdi', 'csho', 
                        'lct', 'txdc', 'dpc', 'che', 'dlc', 'ceq', 'seq', 'teq', 'pstk', 'pstkrv', 
                        'pstkl', 'txditc', 'xint', 'xsga', 'ibc', 'dltt', 'mib', 'ib', 'dp']

        VARS_DATA_TYPE = {'gvkey': str, 'tic': str, 'at': float, 'sale': float, 
                          'cogs': float, 'act': float, 'txdi': float, 'csho': float, 
                          'lct': float, 'dltt': float, 'mib': float, 'txdc': float, 
                          'dp': float, 'che': float, 'dlc': float, 'ceq': float, 
                          'seq': float, 'teq': float, 'pstk': float, 'txditc': float, 
                          'xint': float, 'xsga': float, 'ibc': float, 'ib': float, 
                          'year_end': 'datetime64[ns]', 'years_in': 'Int32', 
                          'quarter_end': 'datetime64[ns]', 'quarters_in': 'Int32', 
                          'ps': float, 'be': float, 'earn': float, 'op': float, 
                          'profit': float, 'inv': float, 'cf': float, 'ac': float, 
                          'nsi': float, 'eg': float, 'grs': float, 'grb': float,
                          'datadate': 'datetime64[ns]', 'fyear': 'Int32'}

        DEFAULT_ID = 'gvkey'
        DEFAULT_DATE = 'datadate'
        DEFAULT_INDFMT = ['INDL']  # default: Industrial, Financial
        DEFAULT_DATAFMT = ['STD']  # default: Standard
        DEFAULT_POPSRC = ['D']      # default: Consolidated
        DEFAULT_CONSOL = ['C']     # default: Consolidated
        ALL_VARS = False

    class COMP_Q:

        TABLE = 'COMP_Q'

        DEFAULT_VARS = ['gvkey', 'datadate', 'tic', 'atq', 'saleq', 'cogsq', 'actq', 
                        'txdiq', 'cshoq', 'lctq', 'txdcy', 'dpcy', 'cheq', 'dlcq', 
                        'ceqq', 'seqq', 'teqq', 'pstkq', 'txditcq', 'xintq', 'xsgaq', 
                        'ibcy', 'dlttq', 'mibq', 'ibq', 'dpq', 'adjex']

        VARS_DATA_TYPE = {'gvkey': str, 'tic': str, 'atq': float, 'saleq': float, 
                          'cogsq': float, 'actq': float, 'txdiq': float, 'cshoq': float, 
                          'lctq': float, 'dlttq': float, 'mibq': float, 'txdcy': float, 
                          'dpre': float, 'cheq': float, 'dlcq': float, 'ceqq': float, 
                          'seqq': float, 'teqq': float, 'pstkq': float, 'txditcq': float, 
                          'xintq': float, 'xsgaq': float, 'ibcy': float, 'ibq': float, 
                          'year_end': 'datetime64[ns]', 'years_in': 'Int32', 
                          'quarter_end': 'datetime64[ns]', 'quarters_in': 'Int32', 
                          'datadate': 'datetime64[ns]', 'fyear': 'Int32', 'adjex': float}

        DEFAULT_ID = 'gvkey'
        DEFAULT_DATE = 'datadate'
        DEFAULT_INDFMT = ['INDL']  # default: Industrial, Financial
        DEFAULT_DATAFMT = ['STD']  # default: Standard
        DEFAULT_POPSRC = ['D']      # default: Consolidated
        DEFAULT_CONSOL = ['C']     # default: Consolidated
        ALL_VARS = False


    class BANK_A:

        TABLE = 'COMP_BANK_A'

        DEFAULT_VARS = ['datadate', 'gvkey', 'cusip', 'conm', 'fic', 'fyr', 'at', 
                        'lt', 'lao', 'lcabg', 'lcacld', 'lcacrd', 'ldt', 'lft', 'lg']

        VARS_DATA_TYPE = {'datadate': 'datetime64[ns]', 'gvkey': str, 'cusip': str, 
                          'conm': str, 'fic': str, 'fyr': 'Int64', 'at': float, 'lt': float, 'lao': float, 
                          'lcabg': float, 'lcacld': float, 'lcacrd': float, 'ldt': float, 
                          'lft': float}

        DEFAULT_ID = 'gvkey'
        DEFAULT_DATE = 'datadate'
        DEFAULT_INDFMT = ['BANK']  # default: Industrial, Financial
        DEFAULT_DATAFMT = ['STD']  # default: Standard
        DEFAULT_POPSRC = ['D']      # default: Consolidated
        DEFAULT_CONSOL = ['C']     # default: Consolidated
        ALL_VARS = False

    class BANK_Q:
        TABLE = None
        VARS_DATA_TYPE = None
        DEFAULT_VARS = None
        DEFAULT_DATE = None
        DEFAULT_ID = None
        ALL_VARS = False

class CCM:

    TABLE = 'CCM'
    
    # if no keyword arguments are given then these are the defaults returned
    DEFAULT_VARS = ['date', 'gvkey', 'permno', 'permco', 'cusip', 'ticker', 'shrcd', 
                    'exchcd', 'datadate', 'year_end', 'ffdate', 
                    'prc', 'shrout', 'adjret', 'adjretx', 'me', 'wt', 'dp', 'be', 
                    'bm', 'ffbm', 'ep', 'ffep', 'cfp', 'ffcfp', 
                    'inv', 'op', 'pr2_12', 'pr1_1', 'pr13_60', 'beta', 'ac', 'nsi', 
                    'years_in', 'months_in', 'month', 'ffyear']
    
    VARS_DATA_TYPE = {'permno': 'Int32', 'permco': 'Int32', 'ticker': str, 'shrcd': 'Int32', 
                      'exchcd': 'Int32', 'prc': float, 'shrout': float, 'adjret': float, 
                      'adjretx': float, 'adjcumret': float, 'adjcumretx': float, 'dp': float, 
                      'year': 'Int32', 'month': 'Int32', 'pr1_1': float, 'pr2_12': float, 
                      'pr13_60': float, 'prx1_1': float, 'prx2_12': float, 'prx13_60': float, 
                      'me': float, 'ffyear': float, 'Int32': 'Int32', 'months_in': 'Int32', 
                      'wt': float, 'dec_me': float, 'dltt': float, 'mib': float, 'revt': float, 
                      'csho': float, 'adjex_f': float, 'act': float, 'xint': float, 
                      'pstk': float, 'txdi': float, 'gvkey': str, 'ib': float, 'xsga': float, 
                      'dlc': float, 'ceq': float, 'che': float, 'txdc': float, 'dpc': float, 
                      'ibc': float, 'fyear': 'Int32', 'pstkl': float, 'teq': float, 
                      'cogs': float, 'pstkrv': float, 'lct': float, 'dpre': float, 'txditc': float, 
                      'seq': float, 'at': float, 'sale': float, 'years_in': 'Int32', 'ps': float, 
                      'be': float, 'earn': float, 'profit': float, 'op': float, 
                      'inv': float, 'cf': float, 'csho_adj': float, 'd_owcap_adj': float, 'ac': float, 
                      'ni_csho_adj': float, 'nsi': float, 'ffbm': float, 'bm': float, 'ffep': float, 
                      'ep': float, 'ffcfp': float, 'cfp': float, 'beta': float, 'lev': float, 
                      'year_end': 'datetime64[ns]', 'ffdate': 'datetime64[ns]', 
                      'datadate': 'datetime64[ns]', 'date': 'datetime64[ns]', 'cusip': str, 'sp': float, 
                      'ffsp': float}
    
    DEFAULT_ID = 'permco'
    DEFAULT_DATE = 'date'
    ALL_VARS = True
    
