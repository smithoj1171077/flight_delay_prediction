DTYPE_MAPPING={
    "continuous": [
        "latitude",
        "longitude",
        "review_scores_rating",
        "review_scores_accuracy",
        "review_scores_cleanliness",
        "review_scores_checkin",
        "review_scores_communication",
        "review_scores_location",
        "review_scores_value",
        "reviews_per_month",
        "host_response_rate",
        "host_acceptance_rate",
        "estimated_revenue_l365d"
    ],
    "discrete": [
        "listing_id",
        "host_id",
        "host_listings_count",
        "host_total_listings_count",
        "accommodates",
        "bathrooms",
        "bedrooms",
        "beds",
        "minimum_nights",
        "maximum_nights",
        "minimum_minimum_nights",
        "maximum_minimum_nights",
        "minimum_maximum_nights",
        "maximum_maximum_nights",
        "minimum_nights_avg_ntm",
        "maximum_nights_avg_ntm",
        "availability_30",
        "availability_60",
        "availability_90",
        "availability_365",
        "number_of_reviews",
        "number_of_reviews_ltm",
        "number_of_reviews_l30d",
        "availability_eoy",
        "number_of_reviews_ly",
        "estimated_occupancy_l365d",
        "calculated_host_listings_count",
        "calculated_host_listings_count_entire_homes",
        "calculated_host_listings_count_private_rooms",
        "calculated_host_listings_count_shared_rooms"
    ],
    "date": [
        "last_scraped",
        "host_since",
        "calendar_last_scraped",
        "first_review",
        "last_review"
    ],
    "location": [
        "host_location", # split this into two columns, and find lon & lat for each column
        "host_neighbourhood",
        "neighbourhood_cleansed" 
    ],
    "nominal": [
        "host_response_time",
        "room_type"
    ],
    "boolean": [
        "host_is_superhost",
        "host_has_profile_pic",
        "host_identity_verified",
        "has_availability",
        "instant_bookable"
    ],
    "text": [
        "name",
        "description",
        "neighborhood_overview",
        "host_about",
        "bathrooms_text", # planning to split into numeric and text columns, tokenise text, then multihot
        "property_type", # planning to tokenise text, then mutihot
    ]
}