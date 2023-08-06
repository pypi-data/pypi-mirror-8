@database.default
Feature: Import transactions
  As a user
  I want to import transactions from a file
  In order to add them to an account quickly

  Scenario: Import transactions in CSV format from ing
    Given the following accounts
      | name     | number    |
      | account1 | 987654321 |
    And a file named '~/.bdgt/import.yaml' doesn't exist
    And a file named "test.csv" with:
      """
      "Datum","Naam / Omschrijving","Rekening","Tegenrekening","Code","Af Bij","Bedrag (EUR)","MutatieSoort","Mededelingen"
      "20150801","Naam en omsch.","987654321","11112222","BA","Af","12,75","Betaalautomaat","Mededelingen hier"
      "20150802","Naam en omsch.","987654321","12321232","GT","Bij","8,50","Internetbankieren","Mededelingen hier"
      """
    When I run "bdgt import file csv-ing test.csv"
    Then the command output should equal:
      """
      Parsed 2 transactions from test.csv.
      """
    And a file named '~/.bdgt/import.yaml' was created
    And the command exit code should be 0

  Scenario: Import MT940
    Given the following accounts
      | name     | number    |
      | account1 | 987654321 |
    And a file named '~/.bdgt/import.yaml' doesn't exist
    And a file named "test.mt940" with:
      """
      ABNANL2A
      940
      ABNANL2A
      :20:ABN AMRO BANK NV
      :25:123456789
      :28:13501/1
      :60F:C120511EUR5138,61
      :61:1205120514C500,01N654NONREF
      987654321
      :86:/TRTP/SEPA OVERBOEKING/IBAN/FR12345678901234/BIC/GEFRADAM
      /NAME/QASD JGRED/REMI/description lines/EREF/NOTPRO
      VIDED
      :62F:C120514EUR5638,62
      """
    When I run "bdgt import file mt940 test.mt940"
    Then the command output should contain:
      """
      Parsed 1 transactions from test.mt940.
      """
    And a file named '~/.bdgt/import.yaml' was created
    And the command exit code should be 0

  Scenario: Import OFX
    Given the following accounts
      | name     | number    |
      | account1 | 987654321 |
    And a file named '~/.bdgt/import.yaml' doesn't exist
    And a file named "test.ofx" with:
      """
      <OFX>
        <SIGNONMSGSRSV1>
          <SONRS>
            <STATUS>
              <CODE>0
              <SEVERITY>INFO
            </STATUS>
            <DTSERVER>20071015021529.000[-8:PST]
            <LANGUAGE>ENG
            <DTACCTUP>19900101000000
            <FI>
              <ORG>MYBANK
              <FID>01234
            </FI>
          </SONRS>
        </SIGNONMSGSRSV1>
        <BANKMSGSRSV1>
            <STMTTRNRS>
              <TRNUID>23382938
              <STATUS>
                <CODE>0
                <SEVERITY>INFO
              </STATUS>
              <STMTRS>
                <CURDEF>USD
                <BANKACCTFROM>
                  <BANKID>987654321
                  <ACCTID>098-121
                  <ACCTTYPE>SAVINGS
                </BANKACCTFROM>
                <BANKTRANLIST>
                  <DTSTART>20070101
                  <DTEND>20071015
                  <STMTTRN>
                    <TRNTYPE>CREDIT
                    <DTPOSTED>20070315
                    <DTUSER>20070315
                    <TRNAMT>200.00
                    <FITID>980315001
                    <NAME>DEPOSIT
                    <MEMO>automatic deposit
                  </STMTTRN>
                </BANKTRANLIST>
                <LEDGERBAL>
                  <BALAMT>5250.00
                  <DTASOF>20071015021529.000[-8:PST]
                </LEDGERBAL>
                <AVAILBAL>
                  <BALAMT>5250.00
                  <DTASOF>20071015021529.000[-8:PST]
                </AVAILBAL>
              </STMTRS>
            </STMTTRNRS>
        </BANKMSGSRSV1>
      </OFX>
      """
    When I run "bdgt import file ofx test.ofx"
    Then the command output should equal:
      """
      Parsed 1 transactions from test.ofx.
      """
    And a file named '~/.bdgt/import.yaml' was created
    And the command exit code should be 0

  Scenario: Import transactions and commit to the database immediately
    Given the following accounts
      | name     | number    |
      | account1 | 987654321 |
    And a file named '~/.bdgt/import.yaml' doesn't exist
    And a file named "test.mt940" with:
      """
      ABNANL2A
      940
      ABNANL2A
      :20:ABN AMRO BANK NV
      :25:123456789
      :28:13501/1
      :60F:C120511EUR5138,61
      :61:1205120514C500,01N654NONREF
      987654321
      :86:/TRTP/SEPA OVERBOEKING/IBAN/FR12345678901234/BIC/GEFRADAM
      /NAME/QASD JGRED/REMI/description lines/EREF/NOTPRO
      VIDED
      :62F:C120514EUR5638,62
      """
    When I run "bdgt import --commit file mt940 test.mt940"
    Then the command output should contain:
      """
      1 transactions imported.
      """
    And a file named '~/.bdgt/import.yaml' was deleted
    And the command exit code should be 0

  Scenario: Show an error message when importing when a previous import hasn't
            been processed.
    Given the following accounts
      | name     | number    |
      | account1 | 987654321 |
    And a file named "~/.bdgt/import.yaml" with:
      """
      content isn't important
      """
    And a file named "test.mt940" with:
      """
      content isn't important
      """
    When I run "bdgt import file mt940 test.mt940"
    Then the command output should equal:
      """
      Error: A previous import has not been processed.
      """
    And the command exit code should be 1

  Scenario: View the status of an import containing unprocessed transactions
    Given a file named "~/.bdgt/import.yaml" with:
      """
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-01
        - !!python/object/apply:decimal.Decimal ['10.00']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: false
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-02
        - !!python/object/apply:decimal.Decimal ['5.25']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: false
      """
    When I run "bdgt import status"
    Then the command output should equal:
      """
      Transactions ready for processing:

      | 1 | 2014-01-01 | 123456 | description |  | [32m10.00[39m |
      | 2 | 2014-01-02 | 123456 | description |  |  [32m5.25[39m |
      """
    And the command exit code should be 0

  Scenario: View the status of an import containing processed transactions
    Given a file named "~/.bdgt/import.yaml" with:
      """
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-01
        - !!python/object/apply:decimal.Decimal ['10.00']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: true
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-02
        - !!python/object/apply:decimal.Decimal ['5.25']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: true
      """
    When I run "bdgt import status"
    Then the command output should equal:
      """
      Transactions ready to commit:

      | 1 | 2014-01-01 | 123456 | description |  | [32m10.00[39m |
      | 2 | 2014-01-02 | 123456 | description |  |  [32m5.25[39m |
      """
    And the command exit code should be 0

  Scenario: View the status of an import containing processed and unprocessed
            transactions
    Given a file named "~/.bdgt/import.yaml" with:
      """
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-01
        - !!python/object/apply:decimal.Decimal ['10.00']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: false
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-02
        - !!python/object/apply:decimal.Decimal ['5.25']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: true
      """
    When I run "bdgt import status"
    Then the command output should equal:
      """
      Transactions ready to commit:

      | 2 | 2014-01-02 | 123456 | description |  | [32m5.25[39m |

      Transactions ready for processing:

      | 1 | 2014-01-01 | 123456 | description |  | [32m10.00[39m |
      """
    And the command exit code should be 0

  Scenario: Add parsed transactions to the staging area
    Given the following accounts
      | name     | number |
      | account1 | 123456 |
    Given a file named "~/.bdgt/import.yaml" with:
      """
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-01
        - !!python/object/apply:decimal.Decimal ['10.00']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: false
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-02
        - !!python/object/apply:decimal.Decimal ['5.25']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: false
      """
    When I run "bdgt import add 1,2"
    Then the command output should equal:
      """
      2 transactions added to the staging area.
      """
    And the content of the file '~/.bdgt/import.yaml' equals:
      """
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-01
        - !!python/object/apply:decimal.Decimal ['10.00']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: true
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-02
        - !!python/object/apply:decimal.Decimal ['5.25']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: true

      """
    And the command exit code should be 0

  Scenario: Report an error when adding transactions with an invalid account
            number
    Given the following accounts
      | name     | number |
      | account1 | 98765  |
    Given a file named "~/.bdgt/import.yaml" with:
      """
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-01
        - !!python/object/apply:decimal.Decimal ['10.00']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: false
      """
    When I run "bdgt import add 1,2"
    Then the command output should equal:
      """
      Error: Account number '123456' does not exist.
      """
    And the command exit code should be 1

  Scenario: Remove a parsed transaction from the staging area
    Given a file named "~/.bdgt/import.yaml" with:
      """
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-01
        - !!python/object/apply:decimal.Decimal ['10.00']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: true
      """
    When I run "bdgt import remove 1"
    Then the command output should equal:
      """
      1 transactions removed from the staging area.
      """
    And the command exit code should be 0

  Scenario: Reset the import process
    Given a file named "~/.bdgt/import.yaml" with:
      """
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-01
        - !!python/object/apply:decimal.Decimal ['10.00']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: true
      """
    When I run "bdgt import reset"
    Then the command output should equal:
      """
      Import process reset successfully.
      """
    And a file named '~/.bdgt/import.yaml' was deleted
    And the command exit code should be 0

  Scenario: Commit imports to the database
    Given the following accounts
      | name     | number |
      | account1 | 123456 |
    And a file named "~/.bdgt/import.yaml" with:
      """
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-01
        - !!python/object/apply:decimal.Decimal ['10.00']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: true
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-02
        - !!python/object/apply:decimal.Decimal ['5.25']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: true
      """
    When I run "bdgt import commit"
    Then the command output should equal:
      """
      2 transactions imported.
      """
    And a file named '~/.bdgt/import.yaml' was deleted
    And the command exit code should be 0

  Scenario: Set the value of a field of parsed transactions
    Given a file named "~/.bdgt/import.yaml" with:
      """
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-01
        - !!python/object/apply:decimal.Decimal ['10.00']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: false
      """
    And the following categories:
      | name | parent |
      | cat1 |        |
    When I run "bdgt import set category cat1 1"
    Then the command output should equal:
      """
      1 transactions updated.
      """
    And the command exit code should be 0

  Scenario: Report an error when setting the category of a parsed transaction
            to a category that doesn't exist.
    Given the following accounts
      | name | number    |
      | test | 987654321 |
    And a file named "~/.bdgt/import.yaml" with:
      """
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-01
        - !!python/object/apply:decimal.Decimal ['10.00']
        - !!python/unicode '987654321'
        - !!python/unicode 'description'
        _processed: false
      """
    When I run "bdgt import set category cat1 1"
    Then the command output should equal:
      """
      Error: Category 'cat1' not found.
      """
    And the command exit code should be 1

  Scenario: Show an error when setting the value of a field for processed
            transactions.
    Given a file named "~/.bdgt/import.yaml" with:
      """
      - !!python/object:bdgt.importer.types.ImportTx
        _category: !!python/unicode ''
        _parsed_tx: !!python/object/new:bdgt.importer.types.ParsedTx
        - 2014-01-01
        - !!python/object/apply:decimal.Decimal ['10.00']
        - !!python/unicode '123456'
        - !!python/unicode 'description'
        _processed: true
      """
    When I run "bdgt import set category cat1 1"
    Then the command output should equal:
      """
      Error: Transaction must not be in the staging area.
      """
    And the command exit code should be 1
