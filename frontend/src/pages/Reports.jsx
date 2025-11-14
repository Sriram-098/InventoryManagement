import React, { useState, useEffect } from 'react'
import { reportService } from '../services/api'

function Reports() {
  const [stats, setStats] = useState(null)
  const [categoryStats, setCategoryStats] = useState([])
  const [recentActivity, setRecentActivity] = useState([])
  const [lowStock, setLowStock] = useState([])
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    loadReports()
  }, [])

  const loadReports = async () => {
    try {
      const [statsRes, categoryRes, activityRes, lowStockRes] = await Promise.all([
        reportService.getStats(),
        reportService.getCategoryStats(),
        reportService.getRecentActivity(7),
        reportService.getLowStock()
      ])

      setStats(statsRes.data)
      setCategoryStats(categoryRes.data)
      setRecentActivity(activityRes.data)
      setLowStock(lowStockRes.data)
    } catch (error) {
      console.error('Error loading reports:', error)
    }
  }

  if (!stats) {
    return <div>Loading reports...</div>
  }

  return (
    <div>
      <h2 style={{ marginBottom: '20px' }}>Inventory Reports</h2>

      <div className="tabs">
        <button
          className={activeTab === 'overview' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={activeTab === 'categories' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('categories')}
        >
          By Category
        </button>
        <button
          className={activeTab === 'activity' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('activity')}
        >
          Recent Activity
        </button>
        <button
          className={activeTab === 'lowstock' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('lowstock')}
        >
          Low Stock Alert
        </button>
      </div>

      {activeTab === 'overview' && (
        <div>
          <div className="stats">
            <div className="stat-card">
              <h3>Total Products</h3>
              <div className="value">{stats.total_products}</div>
            </div>
            <div className="stat-card">
              <h3>Total Value</h3>
              <div className="value">${stats.total_value.toFixed(2)}</div>
            </div>
            <div className="stat-card">
              <h3>Low Stock Items</h3>
              <div className="value low-stock">{stats.low_stock_items}</div>
            </div>
            <div className="stat-card">
              <h3>Out of Stock</h3>
              <div className="value out-of-stock">{stats.out_of_stock_items}</div>
            </div>
            <div className="stat-card">
              <h3>Categories</h3>
              <div className="value">{stats.total_categories}</div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'categories' && (
        <div className="table">
          <table>
            <thead>
              <tr>
                <th>Category</th>
                <th>Product Count</th>
                <th>Total Value</th>
              </tr>
            </thead>
            <tbody>
              {categoryStats.map((cat, idx) => (
                <tr key={idx}>
                  <td>{cat.category}</td>
                  <td>{cat.product_count}</td>
                  <td>${cat.total_value.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === 'activity' && (
        <div className="table">
          <table>
            <thead>
              <tr>
                <th>Action</th>
                <th>Performed By</th>
                <th>Notes</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {recentActivity.map((activity) => (
                <tr key={activity.id}>
                  <td><strong>{activity.action}</strong></td>
                  <td>{activity.performed_by}</td>
                  <td>{activity.notes}</td>
                  <td>{new Date(activity.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === 'lowstock' && (
        <div className="table">
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
              {lowStock.map((product) => (
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
      )}
    </div>
  )
}

export default Reports
