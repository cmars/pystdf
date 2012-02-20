===========================================================
Standard Test Data Format (STDF Specification Version 4)
===========================================================

Introduction to STDF
====================
As the ATE industry matures, many vendors offer networking systems that
complement the test systems themselves and help customers get more out of their
ATE investment. Many of these networking systems are converging on popular
standards, such as EthernetÛ .  A glaring hole in these standards has been
the lack of test result data compatibility between test systems of different
manufacturers, and sometimes within the product lines of a single manufacturer.
In order to help overcome this problem, Teradyne has developed a simple,
flexible, portable data format to which existing data files and formats
can be easily and economically converted. Called the Standard Test Data
Format (STDFÛ ), its specification is contained in the following document.
It is our hope that both users and manufacturers of semiconductor ATE will
find this standard useful, and will incorporate it into their own operations
and products. Teradyne has adopted this standard for the test result output
of all of its UNIXÛ operating system based testers, and offers conversion
software for users of its Test System Director for our other semiconductor
test systems. Teradyne derives no direct commercial benefit from propagating
this standard, but we hope its usefulness, thoroughness, and full documentation
will make all of us who work with ATE more productive.


Teradyne's Use of the STDF Specification
----------------------------------------
The Standard Test Data Format is intended as a comprehensive standard for the
entire ATE industry, not as a description of how Teradyne writes or analyzes
test result data. A test system can support STDF without using all the STDF
record types or filling in all the fields of the record types it does use.
Similarly, when the specification says that an STDF record type can be used
to create a certain report, it cannot be assumed that Teradyne data analysis
software always uses the record type to create its reports. In addition,
the statement that a field or record is required or optional applies only
to the definition of a valid STDF file; data analysis software may require a
field that is declared optional in the specification.  For this reason, the
STDF specification is not the final reference on how any piece of Teradyne
software implements the specification. To determine how a Teradyne test
system fills in the STDF record types, please refer to the documentation
for that test system's executive software. To determine what STDF fields
are used by a Teradyne data analysis tool, refer to the documentation for
the data analysis product.

STDF Design Objectives
======================
As ATE networking continues to emerge into a heterogeneous environment
involving various sophisticated computers and operating systems, it becomes
necessary to define a common ground that allows testers, database and database
management systems, and data analysis software to store and communicate test
data in a form that is useful, general, and flexible.

The Standard Test Data Format (STDF) described in this document provides
such a form. STDF is flexible enough to meet the needs of the different
testers that generate raw test data, the databases that store the data, and
the data analysis programs that use the data. The fact that it is a single,
coherent standard also facilitates the sharing and communicating of the data
among these various components of the complete ATE system.

STDF is not an attempt to specify a database architecture for either testers
or the centralized database engines. Instead, it is a set of logical record
types. Because data items are described in terms of logical record types,
the record types can be used as the underlying data abstraction, whether the
data resides in a data buffer, resides on a mass storage device, or is being
propagated in a network message. It is independent of network or database
architecture. Furthermore, the STDF logical record types may be treated as a
convenient data object by any of the software, either networking or database,
that may be used on a tester or database engine.

Using a standard but flexible test data format makes it possible for a single
data formatting program running on the centralized database engine to accept
data from a wide range of testers, whether the testers come from one vendor
or from different vendors or are custom-built by the ATE user. In addition,
adherence to a standard format permits the exporting of data from the central
database and data analysis engine to the user's in-house network for further
analysis in a form that is well documented and thoroughly debugged. Finally,
the standard makes it possible to develop portable software for data reporting
and analysis on both the testers and the centralized database engine.


The following list summarizes the major objectives that guided the design
of STDF:

* Be capable of storing test data for all semiconductor testers and trimmers.
* Provide a common format for storage and transmission of data.
* Provide a basis for portable data reporting and analysis software.
* Decouple data message format and database format to allow enhancements to
  either, independently of the other.
* Provide support for optional (missing or invalid) data.
* Provide complete and concise documentation for developers and users.
* Make it easy for customers to write their own reports or reformat data for
  their own database.

STDF is already a standard within Teradyne:

* All Teradyne semiconductor testers produce raw data in a format that conforms
  to STDF.
* The Manufacturing Data Pipeline and Insight Series software can process any
  data written in conformance with STDF.

STDF Record Structure
=====================
This section describes the basic STDF V4 record structure.

It describes the following general topics, which
are applicable to all the record types:

* STDF record header
* Record types and subtypes
* Data type codes and representation
* Optional fields and missing/invalid data

STDF Record Header
------------------

Each STDF record begins with a record header consisting of the following
three fields:

=======  =======================================================================
Field    Description
=======  =======================================================================
REC_LEN  The number of bytes of data following the record header. REC_LEN does
         not include the four bytes of the record header.
REC_TYP  An integer identifying a group of related STDF record types.
REC_SUB  An integer identifying a specific STDF record type within each REC_TYP
         group. On REC_TYP and REC_SUB , see the next section.
=======  =======================================================================

Record Types and Subtypes
-------------------------

The header of each STDF record contains a pair of fields called **REC_TYP** and
**REC_SUB**. Each **REC_TYP** value identifies a group of related STDF record
types. Each **REC_SUB** value identifies a single STDF record type within a
**REC_TYP** group. The combination of **REC_TYP** and **REC_SUB** values
uniquely identifies each record type. This design allows groups of related
records to be easily identified by data analysis programs, while providing
unique identification for each type of record in the file.

All **REC_TYP** and **REC_SUB** codes less than 200 are reserved for future use
by Teradyne. All codes greater than 200 are available for custom applications
use. The codes are all in decimal values. The official list of codes and
documentation for their use is maintained by Teradyne's Semiconductor CIM
Division (SCD).

The following table lists the meaning of the **REC_TYP** codes currently defined
by Teradyne, as well as the **REC_SUB** codes defined in the STDF specification.

=======  ==================================================================
REC_TYP  Meaning and STDFREC_SUB Codes
=======  ==================================================================
0        Information about the STDF file
           * 10 File Attributes Record (FAR - :class:`pystdf.V4.Far`)
           * 20 Audit Trail Record (ATR - :class:`pystdf.V4.Atr`)
1        Data collected on a per lot basis
           * 10 Master Information Record (MIR - :class:`pystdf.V4.Mir`)
           * 20 Master Results Record (MRR - :class:`pystdf.V4.Mrr`)
           * 30 Part Count Record (PCR - :class:`pystdf.V4.Pcr`)
           * 40 Hardware Bin Record (HBR - :class:`pystdf.V4.Hbr`)
           * 50 Software Bin Record (SBR - :class:`pystdf.V4.Sbr`)
           * 60 Pin Map Record (PMR - :class:`pystdf.V4.Pmr`)
           * 62 Pin Group Record (PGR - :class:`pystdf.V4.Pgr`)
           * 63 Pin List Record (PLR - :class:`pystdf.V4.Plr`)
           * 70 Retest Data Record (RDR - :class:`pystdf.V4.Rdr`)
           * 80 Site Description Record (SDR - :class:`pystdf.V4.Sdr`)
2        Data collected per wafer
           * 10 Wafer Information Record (WIR - :class:`pystdf.V4.Wir`)
           * 20 Wafer Results Record (WRR - :class:`pystdf.V4.Wrr`)
           * 30 Wafer Configuration Record (WCR - :class:`pystdf.V4.Wcr`)
5        Data collected on a per part basis
           * 10 Part Information Record (PIR - :class:`pystdf.V4.Pir`)
           * 20 Part Results Record (PRR  - :class:`pystdf.V4.Prr`)
10       Data collected per test in the test program
           * 30 Test Synopsis Record (TSR - :class:`pystdf.V4.Tsr` )
15       Data collected per test execution
           * 10 Parametric Test Record (PTR - :class:`pystdf.V4.Ptr`)
           * 15 Multiple-Result Parametric Record (MPR - :class:`pystdf.V4.Mpr`)
           * 20 Functional Test Record (FTR - :class:`pystdf.V4.Ftr`)
20       Data collected per program segment
           * 10 Begin Program Section Record (BPS - :class:`pystdf.V4.Bps`)
           * 20 End Program Section Record (EPS - :class:`pystdf.V4.Eps`)
50       Generic Data
           * 10 Generic Data Record (GDR - :class:`pystdf.V4.Gdr`)
           * 30 Datalog Text Record (DTR - :class:`pystdf.V4.Dtr`)
180      Reserved for use by Image software
181      Reserved for use by IG900 software
=======  ==================================================================

Data Type Codes and Representation
----------------------------------

The STDF specification uses a set of data type codes that are concise and
easily recognizable. For example, R*4 indicates a REAL (float) value stored
in four bytes. A byte consists of eight bits of data.  For purposes of this
document, the low order bit of each byte is designated as bit 0 and the high
order bit as bit 7. The following table gives the complete list of STDF data
type codes, as well as the equivalent C language type specifier.

======  ===================================================  ===================
Code    Description                                          C Type Specifier
======  ===================================================  ===================
C*12    Fixed length character string:                       char[12]
          If a fixed length character string does not fill
          the entire field, it must be left-justified and
          padded with spaces.
C*n     Variable length character string:                    char[]
          first byte = unsigned count of bytes to follow
          (maximum of 255 bytes)
C*f     Variable length character string:                    char[]
          string length is stored in another field
U*1     One byte unsigned integer                            unsigned char
U*2     Two byte unsigned integer                            unsigned short
U*4     Four byte unsigned integer                           unsigned long
I*1     One byte signed integer                              char
I*2     Two byte signed integer                              short
I*4     Four byte signed integer                             long
R*4     Four byte floating point number                      float
R*8     Eight byte floating point number                     long float (double)
B*6     Fixed length bit-encoded data                        char[6]
V*n     Variable data type field:
          The data type is specified by a code in the
          first byte, and the data follows
          (maximum of 255 bytes)
B*n     Variable length bit-encoded field:                   char[]
          First byte = unsigned count of bytes to follow
          (maximum of 255 bytes).
          First data item in least significant bit of the
          second byte of the array (first byte is count.)
D*n     Variable length bit-encoded field:                   char[]
          First two bytes = unsigned count of bits to
          follow (maximum of 65,535 bits).
          First data item in least significant bit of the
          third byte of the array (first two bytes are
          count).
          Unused bits at the high order end of the last
          byte must be zero.
N*1     Unsigned integer data stored in a nibble.            char
          First item in low 4 bits, second item in high
          4 bits. If an odd number of nibbles is indicated,
          the high nibble of the byte will be zero. Only
          whole bytes can be written to the STDF file.
kxTYPE  Array of data of the type specified.                 TYPE[]
          The value of *k* (the number of elements in the
          array) is defined in an earlier field in the
          record. For example, an array of short unsigned
          integers is defined as kxU*2.
======  ===================================================  ===================

Note on Time and Date Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The date and time field used in this specification is defined as a four byte
(32 bit) unsigned integer field measuring the number of seconds since midnight
on January 1st, 1970, in the local time zone. This is the UNIX standard base
time, adjusted to the local time zone.  Refer to the Glossary for definitions
of Setup time, Start time, and Finish time as used in STDF.

Note on Data Representation
^^^^^^^^^^^^^^^^^^^^^^^^^^^
When data is shared among systems with unlike central processors, the problem
arises that there is little or no standardization of data representation (that
is, the bit ordering of various data types) among the various processors of
the world. For example, the data representations for DEC, Motorola, Intel,
and IBM computers are all different, even though at least two of them adhere
to the IEEE floating point standard. Moreover, different processors made by
the same company sometimes store data in incompatible ways.

To address this problem, the STDF specification uses a field calledCPU_TYPE in
the File Attributes Record (FAR). This field indicates the type of processor
that wrote the data (for example, Sun series or DEC-11 series). The field
is used as follows:

* When writing an STDF file, a system uses its own native data representation.
  The type of the writing processor is stored in theCPU_TYPE field.
* When reading an STDF file, a system must convert the records to its own
  native data representation as it reads them, if necessary. To do so, it checks
  the value of the CPU_TYPE field in the FAR, which is the first record in the
  file. Then, if the writing CPU's data representation
  is incompatible with its own, it uses a subroutine that reads the next (or
  selected) record and converts the records to its own data representation as
  it reads them.

This approach has the following advantages:

* All testers, trimmers, and hosts can read and write local data using their
  native data representation.
* Testing and local data analysis are not slowed down by performing data
  conversions on any tester.
* Use of a read subroutine makes data conversion transparent at read time.

This approach works for any combination of host and tester processors, provided
that the machines are capable of storing and reading the test data in eight bit
bytes.

Optional Fields and Missing/Invalid Data
----------------------------------------

Certain fields in STDF records are defined as optional. An optional field
must be present in the record, but there are ways to indicate that its value
is not meaningful, that is, that its data should be considered missing or
invalid. There are two such methods:

* Some optional fields have a predefined value that means that the data for the
  field is missing.  For example, if the optional field is a variable-length
  character string, a length byte of 0 means that the data is missing. If
  the field is numeric, a value of -1 may be defined as meaning that the
  data is missing.
* For other optional fields, all possible stored values, including -1, are
  legal. In this case, the STDF specification for the record defines an
  Optional Data bit field. Each bit is used to designate whether an optional
  field in the record contains valid or invalid data. Usually, if the bit
  for an optional field is set, any data in the field is invalid and should
  be ignored.

Optional fields at the end of a record may be omitted in order to save space
on the storage medium. To be omitted, an optional field must have missing
or invalid data, and all the fields following it must be optional fields
containing missing or invalid data. It is never legal to omit an optional
field from the middle of the record.

The specification of each STDF record has a column labelled **Missing/Invalid
Data Flag**.An entry in this column means that the field is optional, and that
the value shown is the way to flag the field's data as missing or invalid. If
the column does not have an entry, the field is required.

Each data type has a standard way of indicating missing or invalid data,
as the following table shows:

+-------------------------------+--------------------------------------------+
| Data Type                     | Missing/Invalid Data Flag                  |
+===============================+============================================+
| Variable-length string        |  Set the length byte to 0.                 |
+-------------------------------+--------------------------------------------+
| Fixed-length character string | Fill the field with spaces.                |
+-------------------------------+--------------------------------------------+
| Fixed-length binary string    | Set a flag bit in an Optional Data byte.   |
+-------------------------------+--------------------------------------------+
| Time and date fields          | Use a binary 0.                            |
+-------------------------------+--------------------------------------------+
| Signed and unsigned integers  | Use the indicated reserved value           |
| and floating point values     | or set a flag bit in an OptionalDatabyte.  |
+-------------------------------+--------------------------------------------+

Note on *Required* and *Optional*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The distinction between required and optional fields applies only to the
definition of a minimally valid STDF file.Itis not a statement about whether
any software (even Teradyne software) requires the field. A field that
is marked optional in the specification may be required by software that
reads or analyzes the STDF file, even if Teradyne has written the software.
In most cases, a minimally valid STDF file will not provide sufficient input
for a piece of analysis software. You will need to fill in some fields or
records that are not marked as required here.  This specification is not
intended to define the data requirements for any analysis software. The only
authority on whether a piece of software requires a certain STDF field or
record is the documentation for that software.


STDF Record Types
=================

This section contains the definitions for the STDF record types. The following
information is provided for each record type:

* a statement of function: how the record type is used in the STDF file.
* a table defining the data fields: first the standard STDF header, then the
  fields specific to this record type. The information includes the field name,
  the data type (see the previous section for the data type codes), a brief
  description of the field, and the flag to indicate missing or invalid data
  (see the previous section for a discussion of optional fields).
* any additional notes on specific fields.
* possible uses for this record type in data analysis reports. Note that this
  entry states only where the record type can be used. It is not a statement
  that the reports listed always use this record type, even if Teradyne has
  written those reports. For definitive information on how any data analysis
  software uses the STDF file, see the documentation for the data analysis
  software.
* frequency with which the record type appears in the STDF file: for example,
  once per lot, once per wafer, one per test, and so forth.
* the location of the record type in the STDF file. See the note on
  *initial sequence* on the next page.

Note on *Initial Sequence*
--------------------------

For several record types, the *Location* says that the record must appear
*after the initial sequence*.  The phrase *initial sequence* refers to
therecords that must appear at thebeginning of the STDFfile.  The requirements
for the initial sequence are as follows:

* Every file must contain one File Attributes Record (FAR), one Master
  Information Record (MIR), one or more Part Count Records (PCR), and one
  Master Results Record (MRR ). All other records are optional.
* The first record in the STDF file must be the File Attributes Record (FAR).
* If one or more Audit Trail Records (ATRs) are used, they must appear
  immediately after the FAR.
* The Master Information Record (MIR) must appear in every
  STDF file. Its location must be after the FAR and the ATR s(if ATRs are used).
* If the Retest Data Record (RDR ) is used, it must appear immediately
  after the MIR.
* If one or more Site Description Records (SDRs) are used,
  they must appear immediately after the MIR and RDR (if the RDR is used).

Given these requirements, every STDF record must contain one of these
initial sequences:

* FAR - MIR
* FAR - ATRs - MIR
* FAR - MIR- RDR
* FAR - ATRs - MIR- RDR
* FAR - MIR - SDRs
* FAR - ATRs - MIR - SDRs
* FAR - MIR- RDR - SDRs
* FAR - ATRs - MIR- RDR- SDRs

All other STDF record types appear after the initial sequence.

Alphabetical Listing
--------------------

In this section, the STDF record types appear in order of ascending record
type and record subtype codes. For easier reference, the record types are
listed on this page in alphabetical order, by the three-letter abbreviations
for the record types.

======  ====================================  ============
Record  Type                                  PySTDF Class
======  ====================================  ============
ATR     Audit Trail Record                    :class:`pystdf.V4.Atr`
BPS     Begin Program Section Record          :class:`pystdf.V4.Bps`
DTR     Datalog Text Record                   :class:`pystdf.V4.Dtr`
EPS     End Program Section Record            :class:`pystdf.V4.Eps`
FAR     File Attributes Record                :class:`pystdf.V4.Far`
FTR     Functional Test Record                :class:`pystdf.V4.Ftr`
GDR     Generic Data Record                   :class:`pystdf.V4.Gdr`
HBR     Hardware Bin Record                   :class:`pystdf.V4.Hbr`
MIR     Master Information Record             :class:`pystdf.V4.Mir`
MPR     Multiple-Result Parametric Record     :class:`pystdf.V4.Mpr`
MRR     Master Results Record                 :class:`pystdf.V4.Mrr`
PCR     Part Count Record                     :class:`pystdf.V4.Pcr`
PGR     Pin Group Record                      :class:`pystdf.V4.Pgr`
PIR     Part Information Record               :class:`pystdf.V4.Pir`
PLR     Pin List Record                       :class:`pystdf.V4.Plr`
PMR     Pin Map Record                        :class:`pystdf.V4.Pmr`
PRR     Part Results Record                   :class:`pystdf.V4.Prr`
PTR     Parametric Test Record                :class:`pystdf.V4.Ptr`
RDR     Retest Data Record                    :class:`pystdf.V4.Rdr`
SBR     Software Bin Record                   :class:`pystdf.V4.Sbr`
SDR     Site Description Record               :class:`pystdf.V4.Sdr`
TSR     Test Synopsis Record                  :class:`pystdf.V4.Tsr`
WCR     Wafer Configuration Record            :class:`pystdf.V4.Wcr`
WIR     Wafer Information Record              :class:`pystdf.V4.Wir`
WRR     Wafer Results Record                  :class:`pystdf.V4.Wrr`
======  ====================================  ============

