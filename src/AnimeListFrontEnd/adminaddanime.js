import React, { useState, useEffect } from 'react';
import './AddAnimeForm.css'; // Make sure you create a CSS file with the same name
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
const AddAnimeForm = () => {
    const navigate = useNavigate();
    const [animeTypes, setAnimeTypes] = useState([]);
    const [genreTypes, setGenreTypes] = useState([]);
    const [ratings, setRatings] = useState([]);
    const [statuses, setStatuses] = useState([]);
    const [formData, setFormData] = useState({
        title: '',
        category: [],
        animeType: '',
        episodes: '',
        otherTitles: [],
        producers: [],
        rating: '',
        status: '',
        duration: '',
        imageLink: '',
        studios: [],
        summary: ''
    });

    useEffect(() => {
        // Fetch anime types
        fetch('/api/animes/types')
            .then(response => response.json())
            .then(data => setAnimeTypes(data));

        // Fetch genre types
        fetch('/api/genres/types')
            .then(response => response.json())
            .then(data => setGenreTypes(data));

        // Fetch ratings
        fetch('/api/animes/ratings')
            .then(response => response.json())
            .then(data => setRatings(data));

        // Fetch statuses
        fetch('/api/animes/statuses')
            .then(response => response.json())
            .then(data => setStatuses(data));

        // Add catch blocks for error handling...
    }, []);
    const handleDynamicInputChange = (value, index, field) => {
        const updatedItems = [...formData[field]];
        updatedItems[index] = value;
        setFormData({ ...formData, [field]: updatedItems });
    };

    // Function to add a new input field for dynamic fields
    const addDynamicField = (field) => {
        const updatedItems = [...formData[field], ''];
        setFormData({ ...formData, [field]: updatedItems });
    };
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleCheckboxChange = (e) => {
        const { name, value } = e.target;
        const updatedArray = formData[name].includes(value)
            ? formData[name].filter(item => item !== value)
            : [...formData[name], value];
        setFormData({ ...formData, [name]: updatedArray });
    };

    const handleAddField = (e, field) => {
        const updatedArray = [...formData[field], ''];
        setFormData({ ...formData, [field]: updatedArray });
    };

    const handleMultipleInputChange = (e, index, field) => {
        const updatedArray = formData[field].map((item, i) => {
            return i === index ? e.target.value : item;
        });
        setFormData({ ...formData, [field]: updatedArray });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
    
        // You don't need to set headers explicitly, Axios sets the Content-Type to application/json automatically when you pass an object to the data property.
        axios.post('/add_anime', formData)
            .then(response => {
                console.log(response.data);
                navigate('/admin');
            })
            .catch(error => {
                console.error('Error:', error.response ? error.response.data : error.message);
            });
    };

    const addField = (field) => {
        setFormData({ ...formData, [field]: [...formData[field], ''] });
    };

    return (
        <form className="anime-form" onSubmit={handleSubmit}>
            <label>Title:
                <input
                    type="text"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                />
            </label>

            {/* Category Dropdown Populated with Unique 'atype' */}
            <label>Category:
                <select name="category" value={formData.category} onChange={handleInputChange}>
                    <option value="">Select a Category</option>
                    {animeTypes.map((type, index) => (
                        <option key={index} value={type}>{type}</option>
                    ))}
                </select>
            </label>

            {/* Anime Type Dropdown Populated with Unique 'gtype' */}


            <div className="scrollable-section">
                <label>Anime Type:</label>
                {genreTypes.map((type, index) => (  // Assuming genreTypes is an array of types from your backend
                    <label key={index} className="checkbox-label">
                        <input
                            type="checkbox"
                            name="animeType"
                            value={type}
                            checked={formData.animeType.includes(type)}
                            onChange={handleCheckboxChange}
                        />
                        {type}
                    </label>
                ))}
            </div>


            <label>Episodes:
                <input
                    type="number"
                    name="episodes"
                    value={formData.episodes}
                    onChange={handleInputChange}
                />
            </label>

            {/* Dynamically Added 'Other Titles' Fields */}
            <label>Other Titles:</label>
            {formData.otherTitles.map((title, index) => (
                <div key={index} className="input-group">
                    <input
                        type="text"
                        name="otherTitles"
                        value={title}
                        onChange={(e) => handleDynamicInputChange(e.target.value, index, 'otherTitles')}
                    />
                </div>
            ))}
            <button type="button" className="add-button" onClick={() => addDynamicField('otherTitles')}>+</button>
            <label>Producers:</label>
            {formData.producers.map((producer, index) => (
                <div key={index} className="input-group">
                    <input
                        type="text"
                        name="producers"
                        value={producer}
                        onChange={(e) => handleDynamicInputChange(e.target.value, index, 'producers')}
                    />
                </div>
            ))}
            <button type="button" className="add-button" onClick={() => addDynamicField('producers')}>+</button>
            {/* Rating Dropdown Populated with Unique 'rating' */}
            <label>Rating:
                <select name="rating" value={formData.rating} onChange={handleInputChange}>
                    <option value="">Select a Rating</option>
                    {ratings.map((rate, index) => (
                        <option key={index} value={rate}>{rate}</option>
                    ))}
                </select>
            </label>

            {/* Status Dropdown Populated with Unique 'status' */}
            <label>Status:
                <select name="status" value={formData.status} onChange={handleInputChange}>
                    <option value="">Select Status</option>
                    {statuses.map((status, index) => (
                        <option key={index} value={status}>{status}</option>
                    ))}
                </select>
            </label>

            <label>Duration:
                <input
                    type="text"
                    name="duration"
                    value={formData.duration}
                    onChange={handleInputChange}
                />
            </label>

            <label>Image Link:
                <input
                    type="text"
                    name="imageLink"
                    value={formData.imageLink}
                    onChange={handleInputChange}
                />
            </label>

            {/* Dynamically Added 'Studios' Fields */}
            <label>Studios:</label>
            {formData.studios.map((studio, index) => (
                <div key={index} className="input-group">
                    <input
                        type="text"
                        name="studios"
                        value={studio}
                        onChange={(e) => handleDynamicInputChange(e.target.value, index, 'studios')}
                    />
                </div>
            ))}
            <button type="button" className="add-button" onClick={() => addDynamicField('studios')}>+</button>

            <label>Summary:
                <textarea
                    name="summary"
                    value={formData.summary}
                    onChange={handleInputChange}
                />
            </label>

            {/* Aired Dates */}
            <div className="date-label">Aired Dates</div>
            <div className="date-inputs">
                <label>
                    From
                    <input
                        type="date"
                        name="fromDate"
                        value={formData.fromDate}
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    To
                    <input
                        type="date"
                        name="toDate"
                        value={formData.toDate}
                        onChange={handleInputChange}
                    />
                </label>
            </div>

            <button type="submit">Submit</button>
        </form>
    );
};
export default AddAnimeForm;
