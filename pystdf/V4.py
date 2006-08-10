import sys
from PySTDF.Types import StdfRecordMeta, RecordType, stdfToLogicalType
from PySTDF import TableTemplate

import pdb

class Far(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 0
  sub = 10
  fieldMap = (
    ('CPU_TYPE', 'U1'),
    ('STDF_VER', 'U1')
  )
  
class Atr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 0
  sub = 20
  fieldMap = (
    ('MOD_TIM', 'U4'),
    ('CMD_LINE', 'Cn')
  )

class Mir(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 1
  sub = 10
  fieldMap = (
    ('SETUP_T', 'U4'),
    ('START_T', 'U4'),
    ('STAT_NUM', 'U1'),
    ('MODE_COD', 'C1'),
    ('RTST_COD', 'C1'),
    ('PROT_COD', 'C1'),
    ('BURN_TIM', 'U2'),
    ('CMOD_COD', 'C1'),
    ('LOT_ID', 'Cn'),
    ('PART_TYP', 'Cn'),
    ('NODE_NAM', 'Cn'),
    ('TSTR_TYP', 'Cn'),
    ('JOB_NAM', 'Cn'),
    ('JOB_REV', 'Cn'),
    ('SBLOT_ID', 'Cn'),
    ('OPER_NAM', 'Cn'),
    ('EXEC_TYP', 'Cn'),
    ('EXEC_VER', 'Cn'),
    ('TEST_COD', 'Cn'),
    ('TST_TEMP', 'Cn'),
    ('USER_TXT', 'Cn'),
    ('AUX_FILE', 'Cn'),
    ('PKG_TYP', 'Cn'),
    ('FAMLY_ID', 'Cn'),
    ('DATE_COD', 'Cn'),
    ('FACIL_ID', 'Cn'),
    ('FLOOR_ID', 'Cn'),
    ('PROC_ID', 'Cn'),
    ('OPER_FRQ', 'Cn'),
    ('SPEC_NAM', 'Cn'),
    ('SPEC_VER', 'Cn'),
    ('FLOW_ID', 'Cn'),
    ('SETUP_ID', 'Cn'),
    ('DSGN_REV', 'Cn'),
    ('ENG_ID', 'Cn'),
    ('ROM_COD', 'Cn'),
    ('SERL_NUM', 'Cn'),
    ('SUPR_NAM', 'Cn')
  )

class Mrr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 1
  sub = 20
  fieldMap = (
    ('FINISH_T', 'U4'),
    ('DISP_COD', 'C1'),
    ('USR_DESC', 'Cn'),
    ('EXC_DESC', 'Cn')
  )

class Pcr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 1
  sub = 30
  fieldMap = (
    ('HEAD_NUM','U1'),
    ('SITE_NUM','U1'),
    ('PART_CNT','U4'),
    ('RTST_CNT','U4'),
    ('ABRT_CNT','U4'),
    ('GOOD_CNT','U4'),
    ('FUNC_CNT','U4')
  )

class Hbr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 1
  sub = 40
  fieldMap = (
    ('HEAD_NUM','U1'),
    ('SITE_NUM','U1'),
    ('HBIN_NUM','U2'),
    ('HBIN_CNT','U4'),
    ('HBIN_PF','C1'),
    ('HBIN_NAM','Cn')
  )

class Sbr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 1
  sub = 50
  fieldMap = (
    ('HEAD_NUM','U1'),
    ('SITE_NUM','U1'),
    ('SBIN_NUM','U2'),
    ('SBIN_CNT','U4'),
    ('SBIN_PF','C1'),
    ('SBIN_NAM','Cn')
  )

class Pmr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 1
  sub = 60
  fieldMap = (
    ('PMR_INDX','U2'),
    ('CHAN_TYP','U2'),
    ('CHAN_NAM','Cn'),
    ('PHY_NAM','Cn'),
    ('LOG_NAM','Cn'),
    ('HEAD_NUM','U1'),
    ('SITE_NUM','U1')
  )

class Pgr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 1
  sub = 62
  fieldMap = (
    ('GRP_INDX','U2'),
    ('GRP_NAM','Cn'),
    ('INDX_CNT','U2'),
    ('PMR_INDX','k2U2')
  )

class Plr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 1
  sub = 63
  fieldMap = (
    ('GRP_CNT','U2'),
    ('GRP_INDX','k0U2'),
    ('GRP_MODE','k0U2'),
    ('GRP_RADX','k0U1'),
    ('PGM_CHAR','k0Cn'),
    ('RTN_CHAR','k0Cn'),
    ('PGM_CHAL','k0Cn'),
    ('RTN_CHAL','k0Cn')
  )

class Rdr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 1
  sub = 70
  fieldMap = (
    ('NUM_BINS','U2'),
    ('RTST_BIN','k0U2')
  )

class Sdr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 1
  sub = 80
  fieldMap = (
    ('HEAD_NUM','U1'),
    ('SITE_GRP','U1'),
    ('SITE_CNT','U1'),
    ('SITE_NUM','k2U1'),
    ('HAND_TYP','Cn'),
    ('HAND_ID','Cn'),
    ('CARD_TYP','Cn'),
    ('CARD_ID','Cn'),
    ('LOAD_TYP','Cn'),
    ('LOAD_ID','Cn'),
    ('DIB_TYP','Cn'),
    ('DIB_ID','Cn'),
    ('CABL_TYP','Cn'),
    ('CABL_ID','Cn'),
    ('CONT_TYP','Cn'),
    ('CONT_ID','Cn'),
    ('LASR_TYP','Cn'),
    ('LASR_ID','Cn'),
    ('EXTR_TYP','Cn'),
    ('EXTR_ID','Cn')
  )

class Wir(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 2
  sub = 10
  fieldMap = (
    ('HEAD_NUM','U1'),
    ('SITE_GRP','U1'),
    ('START_T','U4'),
    ('WAFER_ID','Cn')
  )

class Wrr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 2
  sub = 20
  fieldMap = (
    ('HEAD_NUM','U1'),
    ('SITE_GRP','U1'),
    ('FINISH_T','U4'),
    ('PART_CNT','U4'),
    ('RTST_CNT','U4'),
    ('ABRT_CNT','U4'),
    ('GOOD_CNT','U4'),
    ('FUNC_CNT','U4'),
    ('WAFER_ID','Cn'),
    ('FABWF_ID','Cn'),
    ('FRAME_ID','Cn'),
    ('MASK_ID','Cn'),
    ('USR_DESC','Cn'),
    ('EXC_DESC','Cn')
  )

class Wcr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 2
  sub = 30
  fieldMap = (
    ('WAFR_SIZ','R4'),
    ('DIE_HT','R4'),
    ('DIE_WID','R4'),
    ('WF_UNITS','U1'),
    ('WF_FLAT','C1'),
    ('CENTER_X','I2'),
    ('CENTER_Y','I2'),
    ('POS_X','C1'),
    ('POS_Y','C1')
  )

class Pir(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 5
  sub = 10
  fieldMap = (
    ('HEAD_NUM','U1'),
    ('SITE_NUM','U1')
  )

class Prr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 5
  sub = 20
  fieldMap = (
    ('HEAD_NUM','U1'),
    ('SITE_NUM','U1'),
    ('PART_FLG','B1'),
    ('NUM_TEST','U2'),
    ('HARD_BIN','U2'),
    ('SOFT_BIN','U2'),
    ('X_COORD','I2'),
    ('Y_COORD','I2'),
    ('TEST_T','U4'),
    ('PART_ID','Cn'),
    ('PART_TXT','Cn'),
    ('PART_FIX','Bn')
  )

class Tsr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 10
  sub = 30
  fieldMap = (
    ('HEAD_NUM','U1'),
    ('SITE_NUM','U1'),
    ('TEST_TYP','C1'),
    ('TEST_NUM','U4'),
    ('EXEC_CNT','U4'),
    ('FAIL_CNT','U4'),
    ('ALRM_CNT','U4'),
    ('TEST_NAM','Cn'),
    ('SEQ_NAME','Cn'),
    ('TEST_LBL','Cn'),
    ('OPT_FLAG','B1'),
    ('TEST_TIM','R4'),
    ('TEST_MIN','R4'),
    ('TEST_MAX','R4'),
    ('TST_SUMS','R4'),
    ('TST_SQRS','R4')
  )

class Ptr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 15
  sub = 10
  fieldMap = (
    ('TEST_NUM','U4'),
    ('HEAD_NUM','U1'),
    ('SITE_NUM','U1'),
    ('TEST_FLG','B1'),
    ('PARM_FLG','B1'),
    ('RESULT','R4'),
    ('TEST_TXT','Cn'),
    ('ALARM_ID','Cn'),
    ('OPT_FLAG','B1'),
    ('RES_SCAL','I1'),
    ('LLM_SCAL','I1'),
    ('HLM_SCAL','I1'),
    ('LO_LIMIT','R4'),
    ('HI_LIMIT','R4'),
    ('UNITS','Cn'),
    ('C_RESFMT','Cn'),
    ('C_LLMFMT','Cn'),
    ('C_HLMFMT','Cn'),
    ('LO_SPEC','R4'),
    ('HI_SPEC','R4')
  )

class Mpr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 15
  sub = 15
  fieldMap = (
    ('TEST_NUM','U4'),
    ('HEAD_NUM','U1'),
    ('SITE_NUM','U1'),
    ('TEST_FLG','B1'),
    ('PARM_FLG','B1'),
    ('RTN_ICNT','U2'),
    ('RSLT_CNT','U2'),
    ('RTN_STAT','k5N1'),
    ('RTN_RSLT','k6R4'),
    ('TEST_TXT','Cn'),
    ('ALARM_ID','Cn'),
    ('OPT_FLAG','B1'),
    ('RES_SCAL','I1'),
    ('LLM_SCAL','I1'),
    ('HLM_SCAL','I1'),
    ('LO_LIMIT','R4'),
    ('HI_LIMIT','R4'),
    ('START_IN','R4'),
    ('INCR_IN','R4'),
    ('RTN_INDX','k5U2'),
    ('UNITS','Cn'),
    ('UNITS_IN','Cn'),
    ('C_RESFMT','Cn'),
    ('C_LLMFMT','Cn'),
    ('C_HLMFMT','Cn'),
    ('LO_SPEC','R4'),
    ('HI_SPEC','R4')
  )

class Ftr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 15
  sub = 20
  fieldMap = (
    ('TEST_NUM','U4'),
    ('HEAD_NUM','U1'),
    ('SITE_NUM','U1'),
    ('TEST_FLG','B1'),
    ('OPT_FLAG','B1'),
    ('CYCL_CNT','U4'),
    ('REL_VADR','U4'),
    ('REPT_CNT','U4'),
    ('NUM_FAIL','U4'),
    ('XFAIL_AD','I4'),
    ('YFAIL_AD','I4'),
    ('VECT_OFF','I2'),
    ('RTN_ICNT','U2'),
    ('PGM_ICNT','U2'),
    ('RTN_INDX','k12U2'),
    ('RTN_STAT','k12N1'),
    ('PGM_INDX','k13U2'),
    ('PGM_STAT','k13N1'),
    ('FAIL_PIN','Dn'),
    ('VECT_NAM','Cn'),
    ('TIME_SET','Cn'),
    ('OP_CODE','Cn'),
    ('TEST_TXT','Cn'),
    ('ALARM_ID','Cn'),
    ('PROG_TXT','Cn'),
    ('RSLT_TXT','Cn'),
    ('PATG_NUM','U1'),
    ('SPIN_MAP','Dn')
  )

class Bps(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 20
  sub = 10
  fieldMap = (
    ('SEQ_NAME','Cn'),
  )

class Eps(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 20
  sub = 20
  fieldMap = ()

class Gdr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 50
  sub = 10
  fieldMap = (
    ('GEN_DATA', 'Vn'),
  )

class Dtr(RecordType):
  __metaclass__ = StdfRecordMeta
  typ = 50
  sub = 30
  fieldMap = (
    ('TEXT_DAT', 'Cn'),
  )

far = Far()
atr = Atr()
mir = Mir()
mrr = Mrr()
pcr = Pcr()
hbr = Hbr()
sbr = Sbr()
pmr = Pmr()
pgr = Pgr()
plr = Plr()
rdr = Rdr()
sdr = Sdr()
wir = Wir()
wrr = Wrr()
wcr = Wcr()
pir = Pir()
prr = Prr()
tsr = Tsr()
ptr = Ptr()
mpr = Mpr()
ftr = Ftr()
bps = Bps()
eps = Eps()
gdr = Gdr()
dtr = Dtr()

records = (
  far,
  atr,
  mir,
  mrr,
  pcr,
  hbr,
  sbr,
  pmr,
  pgr,
  plr,
  rdr,
  sdr,
  wir,
  wrr,
  wcr,
  pir,
  prr,
  tsr,
  ptr,
  mpr,
  ftr,
  bps,
  eps,
  gdr,
  dtr
)
