// Helper function to search location using Open-Meteo
export const searchLocation = async (query) => {
    try {
        const response = await fetch(
            `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(query)}&count=10&language=en`
        );

        if (response.ok) {
            const data = await response.json();
            return data.results || [];
        }
    } catch (error) {
        console.warn('Open-Meteo geocoding failed for query:', query, error);
    }
    return [];
};

// Helper function to select the best result (prefer India locations)
export const selectBestResult = (results) => {
    if (!results || results.length === 0) return null;

    // Try to find Indian locations first
    const indiaResult = results.find(result => result.country_code === 'IN');
    const result = indiaResult || results[0];

    return {
        lat: result.latitude,
        lon: result.longitude,
        name: result.name || 'Unknown Location',
        country: result.country || result.admin1 || result.admin2 || 'Unknown'
    };
};

// Helper function to search by pincode using a dedicated API
const searchByPincode = async (pincode) => {
    try {
        // Try Postcode API for Indian pincodes
        const response = await fetch(
            `https://api.postalpincode.in/pincode/${pincode}`
        );

        if (response.ok) {
            const data = await response.json();
            console.log('Pincode API response:', data);

            if (data && data.length > 0 && data[0].Status === 'Success') {
                const postOffices = data[0].PostOffice;
                if (postOffices && postOffices.length > 0) {
                    const postOffice = postOffices[0];
                    // Get the district or city name to geocode
                    const locationName = postOffice.District || postOffice.Block || postOffice.Name;
                    const state = postOffice.State;

                    // Try to geocode the location name
                    const locationQuery = `${locationName} ${state}`;
                    const results = await searchLocation(locationQuery);
                    if (results && results.length > 0) {
                        const result = selectBestResult(results);
                        if (result) {
                            return {
                                ...result,
                                name: `${postOffice.Name} (${pincode})`,
                                pincode: pincode
                            };
                        }
                    }

                    // Fallback to just the location name
                    return {
                        lat: postOffice.Latitude || 0,
                        lon: postOffice.Longitude || 0,
                        name: `${postOffice.Name} (${pincode})`,
                        country: 'India',
                        pincode: pincode
                    };
                }
            }
        }
    } catch (error) {
        console.warn('Pincode search failed:', error);
    }

    throw new Error(`No results found for pincode ${pincode}. Please verify the pincode.`);
};

// Helper function to parse location query for city and district
const parseLocationQuery = (query) => {
    // Common patterns for city, district combinations
    const patterns = [
        /(.+?)\s*,\s*(.+)/,           // city, district
        /(.+?)\s+(district|taluka|taluk|tehsil)\s+(.+)/i, // city district districtname
        /(.+?)\s+(.+)/,               // city district
        /(district|taluka|taluk|tehsil)\s+(.+)/i,         // district districtname
    ];

    for (const pattern of patterns) {
        const match = query.match(pattern);
        if (match) {
            if (pattern.toString().includes('(district|taluka|taluk|tehsil)') && match.length >= 3) {
                // Handle patterns like "Babaleshwar district Bidar"
                return {
                    city: match[1].trim(),
                    district: match[3].trim()
                };
            } else if (match.length >= 3) {
                // Handle patterns like "Babaleshwar, Bidar" or "Babaleshwar Bidar"
                return {
                    city: match[1].trim(),
                    district: match[2].trim()
                };
            } else if (match.length >= 2) {
                // Handle patterns like "district Bidar"
                return {
                    city: '',
                    district: match[2].trim()
                };
            }
        }
    }

    // If no pattern matches, treat the whole query as a city
    return {
        city: query.trim(),
        district: ''
    };
};

// Helper function to generate fuzzy queries for common spelling variations
const generateFuzzyQueries = (query) => {
    const queries = [query];

    // Common spelling variations
    const variations = {
        'aleshwar': 'aleshwar',
        'alesh': 'alesh',
        'leshwar': 'leshwar',
        'lesh': 'lesh',
        'baba': 'baba'
    };

    // Generate variations
    let fuzzyQuery = query;
    Object.keys(variations).forEach(key => {
        if (fuzzyQuery.includes(key)) {
            const value = variations[key];
            queries.push(fuzzyQuery.replace(key, value));
        }
    });

    // Try removing common suffixes
    if (query.endsWith('pur') || query.endsWith('garh') || query.endsWith('bad')) {
        queries.push(query.slice(0, -3));
    }

    return queries;
};

export const geocodeWithFallback = async (query) => {
    console.log('Geocoding query:', query);

    // Check if the query contains a pincode (6 digits) anywhere in the string
    // \b ensures word boundaries so we don't match inside longer numbers
    const pincodePattern = /\b(\d{6})\b/;
    const pincodeMatch = query.match(pincodePattern);

    if (pincodeMatch) {
        // Handle pincode search
        const pincode = pincodeMatch[1];
        console.log('Detected pincode:', pincode);
        try {
            return await searchByPincode(pincode);
        } catch (e) {
            console.warn('Pincode search failed, falling back to name search:', e);
            // Fallback to name search if pincode fails
        }
    }

    // First try the exact query as provided
    let results = await searchLocation(query);
    if (results && results.length > 0) {
        console.log('Found results for exact query:', results);
        return selectBestResult(results);
    }

    // Try appending context (State/Country) for single-word queries
    if (!query.includes(',')) {
        const contextQueries = [
            `${query}, Karnataka`,
            `${query}, India`
        ];

        for (const contextQuery of contextQueries) {
            console.log('Trying context query:', contextQuery);
            results = await searchLocation(contextQuery);
            if (results && results.length > 0) {
                console.log('Found results for context query:', contextQuery, results);
                return selectBestResult(results);
            }
        }
    }

    // If that fails, try parsing the query for city and district
    const parsedQuery = parseLocationQuery(query);
    console.log('Parsed query:', parsedQuery);

    if (parsedQuery.city && parsedQuery.district) {
        // Try various combinations
        const combinations = [
            `${parsedQuery.city} ${parsedQuery.district}`,
            `${parsedQuery.district} ${parsedQuery.city}`,
            `${parsedQuery.city}, ${parsedQuery.district}`,
            parsedQuery.city,
            parsedQuery.district
        ];

        for (const combination of combinations) {
            console.log('Trying combination:', combination);
            results = await searchLocation(combination);
            if (results && results.length > 0) {
                console.log('Found results for combination:', combination, results);
                return selectBestResult(results);
            }
        }
    } else if (parsedQuery.city) {
        // Just try the city if no district was parsed
        console.log('Trying city only:', parsedQuery.city);
        results = await searchLocation(parsedQuery.city);
        if (results && results.length > 0) {
            console.log('Found results for city:', parsedQuery.city, results);
            return selectBestResult(results);
        }
    }

    // Try fuzzy matching for common spelling variations
    const fuzzyQueries = generateFuzzyQueries(query);
    for (const fuzzyQuery of fuzzyQueries) {
        console.log('Trying fuzzy query:', fuzzyQuery);
        results = await searchLocation(fuzzyQuery);
        if (results && results.length > 0) {
            console.log('Found results for fuzzy query:', fuzzyQuery, results);
            return selectBestResult(results);
        }
    }

    // Fallback to OpenWeatherMap API if API key is available
    const apiKey = import.meta.env.VITE_OPENWEATHER_API_KEY;
    if (apiKey) {
        try {
            console.log('Trying OpenWeatherMap API');
            const response = await fetch(
                `https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(query)}&limit=1&appid=${apiKey}`
            );

            if (response.ok) {
                const matches = await response.json();
                console.log('OpenWeatherMap results:', matches);
                if (matches && matches.length > 0) {
                    return { lat: matches[0].lat, lon: matches[0].lon, name: matches[0].name, country: matches[0].country };
                }
            }
        } catch (error) {
            console.warn('OpenWeatherMap geocoding failed:', error);
        }
    }

    throw new Error('No results for that location. Try a nearby city, town, district, or 6-digit pincode.');
};
