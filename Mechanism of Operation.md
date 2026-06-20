# 🔐 HaxKey Verify – Mechanism of Operation

> **© 2026 TAI-DEV — All rights reserved.**

---

## 1. Overview

HaxKey Verify is a license‑validation application based on **hardware fingerprinting** (hardware‑based ID). The software generates a unique, consistent key for each computer and allows the user to send their personal information along with a screenshot to the administrator via a Discord webhook for license confirmation.

---

## 2. Hardware ID (Fingerprint) Generation Mechanism

When the software is launched for the first time (or on every run), it collects a set of hardware parameters that do not change on the same machine, including:

- **CPU ID** (ProcessorId)
- **Hard disk serial number** (Disk Drive Serial)
- **MAC address** of the primary network adapter
- **Computer Name** – may change, but is used as supplementary data.

These parameters are combined into a single string in a fixed order using our **proprietary algorithm**. This value is always identical on every run on the same hardware.

---

## 3. Verification Process and Data Sending to Discord

After the key is generated and displayed on the interface, the user does the following:

1. Enters their name (or other identifying information) into the input field.
2. Clicks the **“Confirm” / “Verify”** button.

At this point, the software automatically performs these steps:

### A. Screenshot Capture
Takes a full‑screen screenshot of the user’s screen at that moment and saves it as a **PNG** or **JPEG** image (depending on configuration).

### B. Information Collection
Collects additional information:
- 🔑 **Generated Key** (format `XXXXX‑XXXXX‑XXXXX`)
- 👤 **User‑entered name**
- 🖥️ **Hardware ID** (full hash string – for admin verification)
- 📅 **Timestamp** (system time zone)
- 🌐 **Public IP address** (if Internet is available, fetched via a public API)
- 🖥️ **Operating system version** (Windows 10/11)
- 🏷️ **Computer Name**

### C. Payload Delivery
Packages all data into a **JSON payload** and sends it to the admin’s Discord webhook via **HTTP POST**. The screenshot is attached either as a file or as a Base64‑encoded string in the `image` field (depending on webhook format; default is `multipart/form‑data`).

### D. User Feedback
- ✅ **Success:** Displays *“Verification request sent to the administrator.”*, (REF check and move player into field)
- ❌ **Failure:** Shows an error message and advises the user to check their network connection.

---

## 4. Information Received on Discord

The admin will receive a webhook message containing the following fields:

| Field | Description |
| :--- | :--- |
| 🔑 **Key** | `XXXXX‑XXXXX‑XXXXX` |
| 👤 **User name** | User‑entered text |
| 🖥️ **Hostname** | Computer name |
| 📅 **Timestamp** | Date and time of request |
| 🌐 **IP** | Public IP address |
| 📷 **Screenshot** | Attached file or image link |
| 🖥️ **OS** | Windows 10 / 11 |

The admin can use this data to cross‑reference with the licensing list and decide whether to activate the license for that machine.

---

## 5. Security and Consistency

- 🔒 The key is generated **only in memory** and is **not saved to disk** (unless the user manually copies it).
- 🛡️ The Hardware ID does **not contain sensitive personal data** – it is based on device serial numbers and **cannot be reversed** to recover the original parameters.
- 🔐 The key generation algorithm is **closed‑source**, but its mechanism is published for **transparency**.
- 🎯 Each machine generates exactly **one unique key**; no two different machines will produce the same key (collision probability is **extremely low**).

---

## 6. Overall Flow (Diagram)

```text
   Launch the software
         │
         ▼
   Collect hardware → Generate ID
         │
         ▼
   Transform → Format key (XXXXX‑XXXXX‑XXXXX)
         │
         ▼
   Display key on the interface
         │
         ▼
   User enters name and clicks Confirm
         │
         ▼
   Take screenshot + collect additional data
         │
         ▼
   Package and send to Discord webhook
         │
         ▼
   Admin receives notification → Review and approve
