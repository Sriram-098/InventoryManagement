import React, { useState, useEffect } from 'react'
import { productService } from '../services/api'

function ProductDetail({ product, onClose, isAdmin }) {
  const [history, setHistory] = useState([])

  useEffect(() => {
    if (isAdmin) {
      loadHistory()
    }
  }, [])

  const loadHistory = async () => {
    try {
      const response = await productService.getHistory(product.id)
      setHistory(response.data)
    } catch (error) {
      console.error('Error loading history:', error)
    }
  }

  return (
    <div className="modal">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Product Details</h2>
          <button className="close-btn" onClick={onClose}>&times;</button>
        </div>
        
        <div className="product-detail">
          <div className="detail-row">
            <strong>SKU:</strong> {product.sku}
          </div>
          <div className="detail-row">
            <strong>Name:</strong> {product.name}
          </div>
          <div className="detail-row">
            <strong>Category:</strong> {product.category || 'N/A'}
          </div>
          <div className="detail-row">
            <strong>Description:</strong> {product.description || 'No description'}
          </div>
          <div className="detail-row">
            <strong>Price:</strong> ${product.price.toFixed(2)}
          </div>
          <div className="detail-row">
            <strong>Quantity Available:</strong> {product.quantity}
          </div>
          <div className="detail-row">
            <strong>Minimum Stock Level:</strong> {product.min_stock_level}
          </div>
          <div className="detail-row">
            <strong>Supplier:</strong> {product.supplier || 'N/A'}
          </div>
          <div className="detail-row">
            <strong>Status:</strong>{' '}
            {product.quantity === 0 ? (
              <span className="out-of-stock">Out of Stock</span>
            ) : product.quantity <= product.min_stock_level ? (
              <span className="low-stock">Low Stock</span>
            ) : (
              <span className="in-stock">Available</span>
            )}
          </div>

          {isAdmin && history.length > 0 && (
            <div style={{ marginTop: '20px' }}>
              <h3>History</h3>
              <div className="history-list">
                {history.map((item) => (
                  <div key={item.id} className="history-item">
                    <div><strong>{item.action}</strong> by {item.performed_by}</div>
                    <div>{item.notes}</div>
                    <div className="history-date">
                      {new Date(item.created_at).toLocaleString()}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div style={{ marginTop: '20px', textAlign: 'right' }}>
          <button className="btn btn-secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

export default ProductDetail
