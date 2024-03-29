# Ignition SCADA

## What is [<img src="https://github.com/HelloMorrisMoss/diagrams_and_images/blob/main/dashboards_and_hmi/ignition_logo_transparent.png" alt="Ignition"  width="90" height="40"/>](https://inductiveautomation.com/downloads/ignition)?

It's a software system created by [<img src="https://inductiveautomation.com/static/images/logos/inductive-automation-logo.png" width="80" height="20"/>](https://inductiveautomation.com) for controlling and collecting data from industrial processes.

## What is in this repo?

Shareable and useful code I've written for use with Ignition. Many are convenience functions or wrappers for common tasks while developing in Ignition. Also, this readme with some information about my work with Ignition.

## Highlights

* Psuedo-tag: for a cleaner, more object-oriented style to interact with a tag.
* PyDataList: for working on DataSets as Python lists, with many extras.
* save_console_code: ever have the Ignition designer's script console freeze up and lose your code? Call this at the top and save it to a file automatically.
* utils: many small convenience functions.


## Example Dashboards and HMIs
These are Ignition projects that I've built that are now in production.

A couple notes:
* These were built for large production displays and screencapped on a personal computer screen, so a few things are displayed a bit cramped.
* Some information is obscured or substituted as it is proprietary or otherwise not fit for public disclosure.

### Epoxy Coating
This was the first interface I built using Ignition. The operators select their work order on a [filtered list](https://github.com/HelloMorrisMoss/diagrams_and_images/blob/main/dashboards_and_hmi/filtered%20workorder%20selection.png) extracted from JD Edwards, the product and corresponding running conditions are loaded from a database, as well as displaying the instructions for how that product should be packed. This interface works with a smart remote for easy input.

![A SCADA Dashboard built using Ignition SCADA. It shows a PDF of packing instructions, a line graph of operation speed over the last 8 hours, a dial display of target and current machine speed, digital displays of operating conditions and materials used, dropdown selectors for operators to select who is working that shift, and several buttons to change settings.](https://github.com/HelloMorrisMoss/diagrams_and_images/blob/main/dashboards_and_hmi/NH_OEE_01.png)

# Supervision
This is a dashboard for supervisors who have to keep an eye on several production departments at the same time. This shows current conditions and trends across three departments for multiple production lines each. The bright red buttons allow the supervisor to drop down into the full HMI interface for that production line (epoxy coating above) for full details and they can interact with the screen as if they were right at the machine, even from offsite. The general manager of production overseeing these supervisors called this interface a "game changer."

![A SCADA Dashboard built using Ignition SCADA. It shows small overview of production conditions for different manufacturing lines in different production departments.](https://github.com/HelloMorrisMoss/diagrams_and_images/blob/main/dashboards_and_hmi/Supervisors%20dashboard.png)

# Lamination
This interface uses data from several other systems, our JDE business ERP and a third party scanning system. The scanner detects regions of the product that need to be removed, they are highlighted on the table on the left with bright red backgrounds. The length line chart has the actual length produced this shift in blue. The red line shows what the projected had been until the current time and then proceeds with what the projected length going forward is based on the product specifications. The colored boxes pull special instructions relevant to operators, supervisors, and quality control. The single row table at the bottom is displaying the most recently produced in-progress material (from JDE) so that the thickness scanner can catch any issues while production can still correct it.

![A SCADA Dashboard built using Ignition SCADA. It shows a table of operation data for ten numbered zones.The background of measurements out of specification are highlighted with bright red backgrounds. There is a line chart showing the forecast length produced and actual length produced. There are colored boxes with instructions for the operators based on the product being produced. There is a single row table at the bottom showing the next source material that should be used.](https://github.com/HelloMorrisMoss/diagrams_and_images/blob/main/dashboards_and_hmi/Lam%20Dashboard.png)
