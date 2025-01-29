import React from 'react';

const Loading = () => {
    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            minHeight: '100vh',
            backgroundColor: '#FEE8E8',
            color: '#333',
        }}>
            <div style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                flex: 1,
                textAlign: 'center',
                padding: '20px',
            }}>
                <h1 style={{
                    fontSize: '24px',
                    marginBottom: '20px',
                    color: '#BD5555',
                    fontWeight: 'bold',
                }}>
                    Chargement des livres...
                </h1>
                <div style={{
                    border: '8px solid #f3f3f3',
                    borderTop: '8px solid #BD5555',
                    borderRadius: '50%',
                    width: '50px',
                    height: '50px',
                    animation: 'spin 2s linear infinite',
                }} />
            </div>

            <style>
                {`
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                `}
            </style>
        </div>
    );
};

export default Loading;
