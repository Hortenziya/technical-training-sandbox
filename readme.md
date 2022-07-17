# An Estate Property module

The module allows you to register a property for sale and propose to fill out a form that includes the following fields: 
-	**Name** (field must be filled)
-	**Postcode**
-	**Property tags** (must be unique, can be ordered manually by name, users can choose from a list, only manager can create their own tags. A property can have many tags and a tag can be assigned to multiple properties.)
-	**Available From** (the date when property will be available for sale. By default availability date is in 3 months and won’t be copied when the record is duplicated)
-	**Property Type** (must be unique, users can choose predefined type from a list)
-	**Expected Price** (must be strictly positive and field is required)
-	**Selling Price** (must be strictly positive and this field is set if offer is accepted, it’s read-only and won’t be copied when the record is duplicated)
-	**Best Offer** (the highest priced bid is automatically added to this field)
-	**Description** (the seller can provide additional info to the buyers)
-	**Rooms** (2 by default)
-	**Living area**
-	**Facades**
-	**Garage**
-	**Garden** (if garden is not marked, garden orientation and garden area are hidden)
-	**Garden** orientation (north by default )
-	**Garden area** (10sqm by default)
-	**Total Area** (it’s sum of the living area and the garden area, calculated automatically)
-	**State** (could be one of four states: "New" (default), "Offer received", "Offer accepted", "Sold" and "Cancelled". It’s displayed using a statusbar widget which is automatically changed according to the state. "Cancelled" properties can’t be sold and "Sold" properties can’t be cancelled.  Also, property can’t be cancelled when status is "Offer received".  Property can be deleted if it’s state is "New" or "Canceled".  When the property state is "Offer Accepted", "Sold" or "Cancelled" adding a new offer isn’t possible).

## Offers

-	**Status** (could be "Accepted" , "Refused" or "Invisible".  When offer is accepted, it is marked by green color and when refused – by red one. The buttons ‘refuse’ and ‘accept’  are invisible once the offer state is set);
-	**Buyer’s name** (can’t be copied);
-	**Price** (the bid price can’t be lower than 90% of the property expected price and lower than in existing offers);
-	**Period of the offer availability** (by default it is 7 days and can be changed in two ways:  specify the number of days or select a period using the calendar).
Offers list view are editable. Also, in offers list view the refused offers are red, and the accepted offers are green. 

## Other Information 

-	**Salesman** (defined during  property creation) 
-	**Buyer** (the buyer’s name is automatically added when his offer is accepted.

## Views

### List view
All properties by default are shown in a **list view**. It presents only available properties, which status is ‘new’ or ‘offer accepted’. Users can change the filter and view all the estates.  Also properties can be grouped by postcode. When property status is ‘offer received’, it is marked by a green color, when property status is ‘offer accepted’ – by green color and bold style. When property status is `sold`, it is shown in light-gray color. List view has next visual components:  postcode, tags, rooms, living area, expected price and selling price.  Properties list view is editable.

### Kanban view
Users can choose the **Kanban properties view**, which includes next fields: expected price, best price, selling price and tags. The best price is only displayed when an offer is in status  `received`, while the selling price is only displayed when an offer is in status` accepted`. By default properties are grouped by type in this case.

**Search view** allows to filter properties using: title, postcode, expected price, living area, number of bedrooms and/or facades.

**Type List view** of the selected property has three fields: name, expected price and state. Property types can be ordered manually by name. Users can view all properties of the selected property type. The view has a stat button which shows the list of all offers related to properties of the given type when it is clicked on.

**Filters**:  ‘Available’ filter is selected by default and searching on the living area returns results where the area is larger or equal to the given value.

### Other Information
**Users**:  The list of available properties are linked to a salesperson and displayed in their user form view.

**Invoice**: When a property is sold, an invoice id issued for the buyer. Each property is invoiced with the next conditions: 6% of selling price and additional 100.00 administrative fees.

## Security

 - we can make employees real-estate agents or real-estate managers.
 - the admin user is a real-estate manager which has full access to all objects.
 - we have a new real-estate agent employee with no access to invoicing or administration. Real-estate agents can't update the property types or tags. They have only read access to types and tags. Agent user is not able to alter types or tags, or to delete properties, but that he can otherwise create or update properties. Also, he can not see the properties exclusive to their colleagues.
 - Employees who are not at least real-estate agents can't see the real-estate application.
 - Nobody has the right to delete properties. 
