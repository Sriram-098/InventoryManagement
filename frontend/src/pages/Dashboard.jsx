import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { productService, reportService } from '../services/api'

function Dashboard({ user }) {
  const [stats, setStats] = useState({
    totalProducts: 0,
    totalValue: 0,
    lowStock: 0,
    outOfStock: 0,
    totalCategories: 0
  })
  const [lowStockProducts, setLowStockProducts] = useState([])
  const navigate = useNavigate()

  const isAdmin = user.role === 'admin'

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      if (isAdmin) {
        const response = await reportService.getStats()
        setStats(response.data)
        
        const lowStockResponse = await reportService.getLowStock()
        setLowStockProducts(lowStockResponse.data.slice(0, 5))
      } else {
        const response = await productService.getAll()
        const products = response.data
        
        const totalProducts = products.length
        const totalValue = products.reduce((sum, p) => sum + (p.price * p.quantity), 0)
        const lowStock = products.filter(p => p.quantity <= p.min_stock_level && p.quantity > 0).length
        const outOfStock = products.filter(p => p.quantity === 0).length
        
        setStats({ totalProducts, totalValue, lowStock, outOfStock, totalCategories: 0 })
      }
    } catch (error) {
      console.error('Error loading stats:', error)
    }
  }

  return (
    <div>
      <h2 style={{ marginBottom: '20px' }}>
        Welcome, {user.username}! 
        {isAdmin ? ' (Admin Dashboard)' : ' (Customer View)'}
      </h2>

      <div className="stats">
        <div className="stat-card">
          <h3>Total Products</h3>
          <div className="value">{stats.totalProducts || stats.total_products}</div>
        </div>
        <div className="stat-card">
          <h3>Total Inventory Value</h3>
          <div className="value">${(stats.totalValue || stats.total_value || 0).toFixed(2)}</div>
        </div>
        <div className="stat-card">
          <h3>Low Stock Items</h3>
          <div className="value low-stock">{stats.lowStock || stats.low_stock_items}</div>
        </div>
        {isAdmin && (
          <>
            <div className="stat-card">
              <h3>Out of Stock</h3>
              <div className="value out-of-stock">{stats.out_of_stock_items}</div>
            </div>
            <div className="stat-card">
              <h3>Categories</h3>
              <div className="value">{stats.total_categories}</div>
            </div>
          </>
        )}
      </div>

      {isAdmin && lowStockProducts.length > 0 && (
        <div style={{ marginTop: '30px' }}>
          <h3>⚠️ Low Stock Alert</h3>
          <div className="table" style={{ marginTop: '15px' }}>
            <table>
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Name</th>
                  <th>Category</th>
                  <th>Current Stock</th>
                  <th>Min Level</th>
                  <th>Supplier</th>
                </tr>
              </thead>
              <tbody>
                {lowStockProducts.map((product) => (
                  <tr key={product.id}>
                    <td>{product.sku}</td>
                    <td>{product.name}</td>
                    <td>{product.category || '-'}</td>
                    <td className="low-stock">{product.quantity}</td>
                    <td>{product.min_stock_level}</td>
                    <td>{product.supplier || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      
      <div style={{ textAlign: 'center', marginTop: '40px' }}>
        <button className="btn btn-primary" onClick={() => navigate('/products')}>
          Browse Products
        </button>
        {isAdmin && (
          <button className="btn btn-success" onClick={() => navigate('/reports')} style={{ marginLeft: '10px' }}>
            View Reports
          </button>
        )}
      </div>
    </div>
  )
}

export default Dashboard
