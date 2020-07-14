# Django Commerce

Django Commerce is a Web Application built using Django which is similar to e-bay style auction that allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a watchlist.

![Commerce] (resources/img/commerce1.jpg)

#### Active Listings

When a user visits `/` route, they can view all the currently active listings. For each of these listings, if a user clicks on any one of them, they will be redirected to that individual listing's page.

#### Watchlist

For users that are signed in, can visit `/watchlist` page from the navigation bar, to be able to see all the listings that they are currently watching. Clicking on any one of those listings will take them to that specific listing's page.

#### Create a new listing

A user can create a new listing by visiting `/createlisting` page. They will be required to provide - `title`, `description`, `starting bid`, `category` and `image url`. Submitting this form would create the new listing in active status and would be displayed in `/` route. 

#### Listing Page

Clicking on the title of any listing takes the user to that specific listing's page. Regardless of whether a user is signed in or not, they can view all the details - `title`, `description`, `current_price`, and an `image` about this listing. But if a user is signed in, they would be able to -  

* Add/Remove this listing from their `watchlist`.
* Add a bid that is greater than `current_price`. If they try to add a bid less than the highest bid, the form shows an error.
* `close` a listing if they are the owner of that listing. Doing so will make the highest bidder the winner for the auction. Once the listing is closed, it can be viewed in the `/inactive` route.
* View the winner for an auction on a closed listing.
* View as well as add comments on a listing.

![Listing] (resources/img/commerce2.jpg)

#### Categories

Users that are signed in would be able to visit `/categories` route to be able to see all listing categories in the application. Clicking on any individual category would show them all the currently active listings in that category.

#### Django Admin

This application's superusers can visit `/admin` route to be able to view, add, edit, and delete any listing, bid and comment. 
