import React, { useEffect, useRef, useState } from 'react';
import { useLocation } from 'react-router-dom';
import './Styles/Content.css';
import axios from 'axios';
import { getUserId } from './429Project/userToken';

export default function Content() {
    const location = useLocation();
    const movie = location.state.movie;
    const [rating, setRating] = useState(0);
    const [hoveredRating, setHoveredRating] = useState(0);

    const starRating = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    useEffect(() => {
        const fetchRating = async () => {
            try{
                const response = await axios.post('api/animes/content/getrate',{anime_id: movie['anime_id'], user_id: getUserId()});
                if (response.status === 200) {
                    setRating(Number(response.data));
                }
            } catch (error) {
                console.error('Error performing search:', error);
            }
        }
        fetchRating();
    });

    if (!movie) return <div>Loading...</div>;

    const handleStarClick = async (starIndex) => {
    try{
        setRating(starIndex);
        const response = await axios.post('api/animes/content/rate',{rating: starIndex, anime_id: movie['anime_id'], user_id: getUserId()});
        if (response.status === 200) {
        }
    } catch (error) {
        console.error('Error performing search:', error);
    }

    
};

const handleStarHover = (starIndex) => {
    setHoveredRating(starIndex);
};


const handleStarLeave = () => {
    setHoveredRating(0);
};



return (
    <div className='contentPage'>
        <div className="movie-card">
            <div className="poster-container">
                <img src={movie['large_image_url']} alt={movie['title']} className="poster" />
            </div>
            {console.log(movie)}
            <div className="info-container" style={{ backgroundColor: 'white' }}>
                <p><strong>Name:</strong> {movie['title']}</p>
                <p><strong>Category:</strong> {movie['atype']}</p>
                <p><strong>Genre:</strong> {movie['genres'].join(', ')}</p>
                <p><strong>Episodes:</strong> {movie['episodes']}</p>
                <p><strong>Status:</strong> {movie['status']}</p>
                <p><strong>Duration:</strong> {movie['duration']}</p>
                <p className='summary'><strong>Summary:</strong> {movie['synopsis']}</p>
                {/* Rating Section */}
                <div className="rating-container">
                    <p><strong>Puanınız:</strong> {rating}/10</p>
                    <div className="stars-container" onMouseLeave={handleStarLeave}>
                        {starRating.map((starIndex) => (
                            <span
                                key={starIndex}
                                className={`star ${starIndex <= (hoveredRating) ? 'selected' : starIndex <= rating ? 'ratingSelected' : ''}`}
                                onClick={() => handleStarClick(starIndex)}
                                onMouseEnter={() => handleStarHover(starIndex)}
                            >
                                &#9733;
                            </span>
                        ))}
                    </div>
                </div>
                <p><strong>Score:</strong> {movie['score']}</p>
                <p><strong>Rank:</strong> {movie['arank']}</p>
                <p><strong>Favorites:</strong> {movie['favorites']}</p>
                <p><strong>Start - Finish Date:</strong> {movie['aired_dates'][0]}</p>
                <p><strong>Producers:</strong> {movie['producers'].join(', ')}</p>
                <p><strong>Studios:</strong> {movie['studios'].join(', ')}</p>
            </div>
        </div>

    </div>
);
}
