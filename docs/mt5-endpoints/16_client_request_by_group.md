# ClientRequestByGroup - Retrieve Client (KYC) Records by Group

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns client (KYC) records for users matching the group mask. Clients are master entities that can be linked to one or more user accounts.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.ClientRequestByGroup(group_mask: str) -> list[MTClient]` |

## Example Code

```python
clients = manager.ClientRequestByGroup("*")
for c in clients:
    print(c.ID, c.Name, c.Email, c.Phone, c.Country, c.Status)
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `AddressCity` | str | `` |
| `AddressCountry` | str | `Turkiye` |
| `AddressPostcode` | str | `` |
| `AddressState` | str | `` |
| `AddressStreet` | str | `` |
| `AssignedManager` | int | `0` |
| `ClientExternalID` | str | `` |
| `ClientOrigin` | int | `4` |
| `ClientOriginLogin` | int | `1010` |
| `ClientStatus` | int | `700` |
| `ClientType` | int | `1` |
| `CompanyAddress` | str | `` |
| `CompanyCountry` | str | `` |
| `CompanyLei` | str | `` |
| `CompanyLicenseAuthority` | str | `` |
| `CompanyLicenseNumber` | str | `` |
| `CompanyName` | str | `` |
| `CompanyRegAuthority` | str | `` |
| `CompanyRegDate` | int | `0` |
| `CompanyRegNumber` | str | `` |
| `CompanyVat` | str | `` |
| `CompanyWebsite` | str | `` |
| `ComplianceApprovedBy` | int | `0` |
| `ComplianceClientCategory` | str | `` |
| `ComplianceDateApproval` | int | `1771739442` |
| `ComplianceDateTermination` | int | `0` |
| `ContactEmail` | str | `adel@forfx.com` |
| `ContactLanguage` | str | `` |
| `ContactLastDate` | int | `0` |
| `ContactMessengers` | str | `` |
| `ContactPhone` | str | `` |
| `ContactPreferred` | int | `0` |
| `ContactSocialNetworks` | str | `` |
| `DateCreated` | int | `1771739442` |
| `DateModified` | int | `1771739442` |
| `ExperienceCFD` | int | `0` |
| `ExperienceFX` | int | `0` |
| `ExperienceFutures` | int | `0` |
| `ExperienceStocks` | int | `0` |
| `Introducer` | str | `` |
| `KYCStatus` | int | `0` |
| `LeadCampaign` | str | `` |
| `LeadSource` | str | `` |
| `PersonAnnualDeposit` | float | `0.0` |
| `PersonAnnualIncome` | float | `0.0` |
| `PersonBirthDate` | int | `0` |
| `PersonCitizenship` | str | `` |
| `PersonDocumentDate` | int | `0` |
| `PersonDocumentExpiration` | int | `0` |
| `PersonDocumentExtra` | str | `` |
| `PersonDocumentNumber` | str | `` |
| `PersonDocumentType` | str | `` |
| `PersonEducation` | int | `0` |
| `PersonEmployment` | int | `0` |
| `PersonGender` | int | `0` |
| `PersonIndustry` | int | `0` |
| `PersonLastName` | str | `Shafia` |
| `PersonMiddleName` | str | `` |
| `PersonName` | str | `Adel` |
| `PersonNetWorth` | float | `0.0` |
| `PersonTaxID` | str | `` |
| `PersonTitle` | str | `` |
| `PersonWealthSource` | int | `0` |
| `RecordID` | int | `1000` |
| `TradingGroup` | str | `real\A\HL\ECNPRO\USD` |


## Raw Sample Response

```json
{
  "AddressCity": "",
  "AddressCountry": "Turkiye",
  "AddressPostcode": "",
  "AddressState": "",
  "AddressStreet": "",
  "AssignedManager": 0,
  "ClientExternalID": "",
  "ClientOrigin": 4,
  "ClientOriginLogin": 1010,
  "ClientStatus": 700,
  "ClientType": 1,
  "CompanyAddress": "",
  "CompanyCountry": "",
  "CompanyLei": "",
  "CompanyLicenseAuthority": "",
  "CompanyLicenseNumber": "",
  "CompanyName": "",
  "CompanyRegAuthority": "",
  "CompanyRegDate": 0,
  "CompanyRegNumber": "",
  "CompanyVat": "",
  "CompanyWebsite": "",
  "ComplianceApprovedBy": 0,
  "ComplianceClientCategory": "",
  "ComplianceDateApproval": 1771739442,
  "ComplianceDateTermination": 0,
  "ContactEmail": "adel@forfx.com",
  "ContactLanguage": "",
  "ContactLastDate": 0,
  "ContactMessengers": "",
  "ContactPhone": "",
  "ContactPreferred": 0,
  "ContactSocialNetworks": "",
  "DateCreated": 1771739442,
  "DateModified": 1771739442,
  "ExperienceCFD": 0,
  "ExperienceFX": 0,
  "ExperienceFutures": 0,
  "ExperienceStocks": 0,
  "Introducer": "",
  "KYCStatus": 0,
  "LeadCampaign": "",
  "LeadSource": "",
  "PersonAnnualDeposit": 0.0,
  "PersonAnnualIncome": 0.0,
  "PersonBirthDate": 0,
  "PersonCitizenship": "",
  "PersonDocumentDate": 0,
  "PersonDocumentExpiration": 0,
  "PersonDocumentExtra": "",
  "PersonDocumentNumber": "",
  "PersonDocumentType": "",
  "PersonEducation": 0,
  "PersonEmployment": 0,
  "PersonGender": 0,
  "PersonIndustry": 0,
  "PersonLastName": "Shafia",
  "PersonMiddleName": "",
  "PersonName": "Adel",
  "PersonNetWorth": 0.0,
  "PersonTaxID": "",
  "PersonTitle": "",
  "PersonWealthSource": 0,
  "RecordID": 1000,
  "TradingGroup": "real\\A\\HL\\ECNPRO\\USD"
}
```
