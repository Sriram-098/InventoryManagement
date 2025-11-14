import React, { useState, useEffect } from 'react'
import { productService } from '../services/api'
import ProductForm from '../components/ProductForm'
import ProductDetail from '../components/ProductDetail'

function Products({ user }) {
  const [products, setProducts] = useState([])
  const [filteredProducts, setFilteredProducts] = useState([])
  const [showModal, setShowModal] = useState(false)
  const [showDetail, setShowDetail] = useState(false)
  const [editingProduct, setEditingProduct] = useState(null)
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [categories, setCategories] = useState([])
  const [filters, setFilters] = useState({
    search: '',
    category: '',
    minPrice: '',
    maxPrice: ''
  })

  const isAdmin = user.role === 'admin'

  useEffect(() => {
    loadProducts()
    loadCategories()
  }, [])

  useEffect(() => {
    applyFilters()
  }, [products, filters])

  const loadProducts = async () => {
    try {
      const response = await productService.getAll()
      setProducts(response.data)
    } catch (error) {
      console.error('Error loading products:', error)
    }
  }

  const loadCategories = async () => {
    try {
      const response = await productService.getCategories()
      setCategories(response.data)
    } catch (error) {
      console.error('Error loading categories:', error)
    }
  }

  const applyFilters = () => {
    let filtered = [...products]

    if (filters.search) {
      filtered = filtered.filter(p =>
        p.name.toLowerCase().includes(filters.search.toLowerCase()) ||
        p.sku.toLowerCase().includes(filters.search.toLowerCase())
      )
    }

    if (filters.category) {
      filtered = filtered.filter(p => p.category === filters.category)
    }

    if (filters.minPrice) {
      filtered = filtered.filter(p => p.price >= parseFloat(filters.minPrice))
    }

    if (filters.maxPrice) {
      filtered = filtered.filter(p => p.price <= parseFloat(filters.maxPrice))
    }

    setFilteredProducts(filtered)
  }

  const handleFilterChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value })
  }

  const clearFilters = () => {
    setFilters({ search: '', category: '', minPrice: '', maxPrice: '' })
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
        await productService.delete(id)
        loadProducts()
      } catch (error) {
        console.error('Error deleting product:', error)
        alert('Error deleting product')
      }
    }
  }

  const handleEdit = (product) => {
    setEditingProduct(product)
    setShowModal(true)
  }

  const handleAdd = () => {
    setEditingProduct(null)
    setShowModal(true)
  }

  const handleViewDetail = (product) => {
    setSelectedProduct(product)
    setShowDetail(true)
  }

  const handleFormSubmit = () => {
    setShowModal(false)
    setEditingProduct(null)
    loadProducts()
  }

  return (
    <div>
      <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Products Catalog</h2>
        {isAdmin && (
          <button className="btn btn-success" onClick={handleAdd}>
            + Add Product
          </button>
        )}
      </div>

      {/* Filters */}
      <div className="filters-panel">
        <div className="filter-group">
          <input
            type="text"
            name="search"
            placeholder="Search by name or SKU..."
            value={filters.search}
            onChange={handleFilterChange}
          />
        </div>
        <div className="filter-group">
          <select name="category" value={filters.category} onChange={handleFilterChange}>
            <option value="">All Categories</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
        <div className="filter-group">
          <input
            type="number"
            name="minPrice"
            placeholder="Min Price"
            value={filters.minPrice}
            onChange={handleFilterChange}
            step="0.01"
          />
        </div>
        <div className="filter-group">
          <input
            type="number"
            name="maxPrice"
            placeholder="Max Price"
            value={filters.maxPrice}
            onChange={handleFilterChange}
            step="0.01"
          />
        </div>
        <button className="btn btn-secondary" onClick={clearFilters}>
          Clear
        </button>
      </div>

      <div style={{ marginBottom: '10px', color: '#7f8c8d' }}>
        Showing {filteredProducts.length} of {products.length} products
      </div>

      <div className="table">
        <table>
          <thead>
            <tr>
              <th>SKU</th>
              <th>Name</th>
              <th>Category</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Supplier</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredProducts.map((product) => (
              <tr key={product.id}>
                <td>{product.sku}</td>
                <td>{product.name}</td>
                <td>{product.category || '-'}</td>
                <td>${product.price.toFixed(2)}</td>
                <td>{product.quantity}</td>
                <td>{product.supplier || '-'}</td>
                <td>
                  {product.quantity === 0 ? (
                    <span className="out-of-stock">Out of Stock</span>
                  ) : product.quantity <= product.min_stock_level ? (
                    <span className="low-stock">Low Stock</span>
                  ) : (
                    <span className="in-stock">In Stock</span>
                  )}
                </td>
                <td>
                  <div className="actions">
                    <button className="btn btn-info" onClick={() => handleViewDetail(product)}>
                      View
                    </button>
                    {isAdmin && (
                      <>
                        <button className="btn btn-primary" onClick={() => handleEdit(product)}>
                          Edit
                        </button>
                        <button className="btn btn-danger" onClick={() => handleDelete(product.id)}>
                          Delete
                        </button>
                      </>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showModal && (
        <ProductForm
          product={editingProduct}
          onClose={() => setShowModal(false)}
          onSubmit={handleFormSubmit}
        />
      )}

      {showDetail && (
        <ProductDetail
          product={selectedProduct}
          onClose={() => setShowDetail(false)}
          isAdmin={isAdmin}
        />
      )}
    </div>
  )
}

export default Products
