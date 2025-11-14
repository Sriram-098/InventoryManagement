/**
 * Unit tests for API service
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import axios from 'axios'
import { authService, productService, reportService } from './api'

// Mock axios
vi.mock('axios')

describe('API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
  })

  describe('authService', () => {
    it('should login successfully', async () => {
      const mockResponse = {
        data: {
          access_token: 'test-token',
          user: { username: 'testuser', role: 'admin' }
        }
      }
      axios.create.mockReturnValue({
        post: vi.fn().mockResolvedValue(mockResponse),
        interceptors: {
          request: { use: vi.fn() }
        }
      })

      const credentials = { username: 'testuser', password: 'password' }
      const result = await authService.login(credentials)
      
      expect(result.data.access_token).toBe('test-token')
      expect(result.data.user.username).toBe('testuser')
    })

    it('should register new user', async () => {
      const mockResponse = {
        data: {
          username: 'newuser',
          email: 'new@example.com',
          role: 'customer'
        }
      }
      axios.create.mockReturnValue({
        post: vi.fn().mockResolvedValue(mockResponse),
        interceptors: {
          request: { use: vi.fn() }
        }
      })

      const userData = {
        username: 'newuser',
        email: 'new@example.com',
        password: 'password',
        role: 'customer'
      }
      const result = await authService.register(userData)
      
      expect(result.data.username).toBe('newuser')
      expect(result.data.role).toBe('customer')
    })
  })

  describe('productService', () => {
    it('should get all products', async () => {
      const mockProducts = [
        { id: 1, name: 'Product 1', price: 10.0, quantity: 50 },
        { id: 2, name: 'Product 2', price: 20.0, quantity: 30 }
      ]
      axios.create.mockReturnValue({
        get: vi.fn().mockResolvedValue({ data: mockProducts }),
        interceptors: {
          request: { use: vi.fn() }
        }
      })

      const result = await productService.getAll()
      
      expect(result.data).toHaveLength(2)
      expect(result.data[0].name).toBe('Product 1')
    })

    it('should create new product', async () => {
      const newProduct = {
        name: 'New Product',
        sku: 'NEW-001',
        price: 99.99,
        quantity: 100
      }
      const mockResponse = { data: { id: 1, ...newProduct } }
      
      axios.create.mockReturnValue({
        post: vi.fn().mockResolvedValue(mockResponse),
        interceptors: {
          request: { use: vi.fn() }
        }
      })

      const result = await productService.create(newProduct)
      
      expect(result.data.id).toBe(1)
      expect(result.data.name).toBe('New Product')
    })

    it('should update product', async () => {
      const updateData = { name: 'Updated Name', price: 150.0 }
      const mockResponse = { data: { id: 1, ...updateData } }
      
      axios.create.mockReturnValue({
        put: vi.fn().mockResolvedValue(mockResponse),
        interceptors: {
          request: { use: vi.fn() }
        }
      })

      const result = await productService.update(1, updateData)
      
      expect(result.data.name).toBe('Updated Name')
      expect(result.data.price).toBe(150.0)
    })

    it('should delete product', async () => {
      const mockResponse = { data: { message: 'Product deleted' } }
      
      axios.create.mockReturnValue({
        delete: vi.fn().mockResolvedValue(mockResponse),
        interceptors: {
          request: { use: vi.fn() }
        }
      })

      const result = await productService.delete(1)
      
      expect(result.data.message).toBe('Product deleted')
    })
  })

  describe('reportService', () => {
    it('should get statistics', async () => {
      const mockStats = {
        total_products: 100,
        total_value: 50000.0,
        low_stock_items: 5,
        out_of_stock_items: 2
      }
      
      axios.create.mockReturnValue({
        get: vi.fn().mockResolvedValue({ data: mockStats }),
        interceptors: {
          request: { use: vi.fn() }
        }
      })

      const result = await reportService.getStats()
      
      expect(result.data.total_products).toBe(100)
      expect(result.data.total_value).toBe(50000.0)
    })
  })
})
