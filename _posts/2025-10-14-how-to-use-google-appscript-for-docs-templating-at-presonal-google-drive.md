---
title: How to use Google AppScript for docs templating at personal Google Drive
date: 2024-02-23T18:44:45+0100
lastmod: 2024-02-23T18:44:45+0100
draft: false
description: "How to use Google AppScript to auto-generate personalized Google Docs letters from a Google Sheets template, replacing placeholders with recipient and sender data."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['bash', 'devopsinuse', 'appscript', 'docs']
categories: ["Linux"]
---

I have recently had a requirement to write quite a few letters. Each letter must have a recipient
address as well as a sender address. I thought to myself that it would make sense to create a spreadsheet in Google Drive
where I would store all the addresses (senders/recipients). Moreover, I had a Google Docs template ready.
I knew that there is something called AppScript from Google that could potentially do the job.

The script below adds a custom menu to Google Sheets. When triggered, it iterates over each row in the spreadsheet, creates a copy of a Google Docs template, and replaces placeholder tags (like `{{Name}}`, `{{Street}}`, etc.) with actual values from the sheet.

```javascript
function onOpen() {                                         /* this function will run when Google Sheets (Gsh) loads, it is a trigger to allow us to add a menu to the Gsh UI */
const ui = SpreadsheetApp.getUi();                        /* returns an instance of the Gsh UI that we can use to add a menu to our Gsh UI */
const menu = ui.createMenu('AutoFill Docs');              /* creates the 'Autofill Docs' menu label */
menu.addItem('Create new docs','createNewGoogleDocs');    /* creates the 'Create new docs' menu item */
menu.addToUi();                                           /* adds the menu and the menu label to Gsh UI */
}

function createNewGoogleDocs() {                                                                    /* will loop through the Gsh rows and generate a new Gdoc if the Document Link Column is empty */
const googleDocTemplate = DriveApp.getFileById('1PD...EEEUTYSV8Uk');   /* get the spreadsheet Id */
const destinationFolder = DriveApp.getFolderById('1v6...');              /* get the Gdoc's folder Id */
// const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Data');                         /* returns the 'Data' sheet of the
const sheet = SpreadsheetApp.openById('1ADZv98424QSS08m8x9s28Lr.....UeHvPE').getSheetByName('Sheet1');
const constants = SpreadsheetApp.openById('1ADZ98424Q...yTUeHvPE').getSheetByName('Constants');
const rows = sheet.getDataRange().getValues();
const personal = constants.getDataRange().getValues()
const k = personal[0]  // K...
const d = personal[1]  // D...

const seller = k
// const seller = d



rows.forEach(function(row, index){                       /* iterates through each row of the 'rows' array variable and returns the index of each element of the array */
if (index === 0) return;                               /* skips the head row (en-tête du tableau)ie element with the 0 index*/
//if (row[3]) return;
const nice = seller[0].split(' ').reverse().join(' ').replace(/\s+/g, '-').toLowerCase()

const googleDocTemplateCopy = googleDocTemplate.makeCopy(`od-${nice}-pre-${row[0].split(' ').reverse().join(' ').replace(/\s+/g, '-').toLowerCase()}`, destinationFolder);     /* make a copy of the spreadsheet named Persona xxx xxx in Destination Folder*/
const openedgoogleDocTemplateCopy = DocumentApp.openById(googleDocTemplateCopy.getId());                         /* open it */
const openedGoogleDocTemplateCopyBody = openedgoogleDocTemplateCopy.getBody();

openedGoogleDocTemplateCopyBody.replaceText('{{Name}}', row[0].split(' ').reverse().join(' '));
openedGoogleDocTemplateCopyBody.replaceText('{{Street}}', row[1]);
openedGoogleDocTemplateCopyBody.replaceText('{{City}}', row[2]);
openedGoogleDocTemplateCopyBody.replaceText('{{ZIP}}', row[3]);

openedGoogleDocTemplateCopyBody.replaceText('{{s-name}}', seller[0].split(' ').reverse().join(' '));
openedGoogleDocTemplateCopyBody.replaceText('{{s-address}}', seller[1]);
openedGoogleDocTemplateCopyBody.replaceText('{{s-city}}', seller[2]);
openedGoogleDocTemplateCopyBody.replaceText('{{s-zip}}', seller[3]);
openedGoogleDocTemplateCopyBody.replaceText('{{s-price}}', seller[5]);
openedGoogleDocTemplateCopyBody.replaceText('{{s-email}}', seller[6]);
openedGoogleDocTemplateCopyBody.replaceText('{{s-phone}}', seller[7]);



openedgoogleDocTemplateCopy.saveAndClose();                      /*make changes permanent*/
const url = openedgoogleDocTemplateCopy.getUrl();                /* get the url of the copy*/
sheet.getRange(index + 1, 6).setValue(url);                       /* set the 'cursor' in the 'Document Link' column and then write the //url*/
}
)

}

```

