import React from 'react';
import HeadBar from "./HeadBar";

const Error = ({ message }) => {
    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            minHeight: '100vh',
            backgroundColor: '#FEE8E8', /* Couleur de fond douce */
            color: '#333',
        }}>
            <div style={{
                backgroundColor: '#FCA5A5', /* Fond pour l'erreur */
                padding: '30px',
                borderRadius: '8px',
                boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)', /* Ombre douce */
                width: '100%',
                maxWidth: '600px',
                margin: '20px auto',
            }}>
                <h1 style={{
                    fontSize: '24px',
                    fontWeight: 'bold',
                    color: '#fff', /* Texte blanc pour le contraste */
                    marginBottom: '10px',
                }}>
                    Oops, quelque chose s'est mal passé!
                </h1>
                <p style={{
                    fontSize: '18px',
                    color: '#fff',
                    margin: '0',
                }}>
                    {message}
                </p>
            </div>
        </div>
    );
};

export default Error;
