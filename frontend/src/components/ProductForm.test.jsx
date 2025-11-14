/**
 * Unit tests for ProductForm component
 */
import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import ProductForm from './ProductForm'
import { productService } from '../services/api'

vi.mock('../services/api')

describe('ProductForm', () => {
  const mockOnClose = vi.fn()
  const mockOnSubmit = vi.fn()

  it('renders add product form', () => {
    render(
      <ProductForm
        product={null}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    )

    expect(screen.getByText('Add New Product')).toBeInTheDocument()
    expect(screen.getByLabelText(/SKU/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/Product Name/i)).toBeInTheDocument()
  })

  it('renders edit product form with data', () => {
    const product = {
      id: 1,
      name: 'Test Product',
      sku: 'TEST-001',
      price: 99.99,
      quantity: 50,
      category: 'Electronics',
      description: 'Test description',
      min_stock_level: 10,
      supplier: 'Test Supplier'
    }

    render(
      <ProductForm
        product={product}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    )

    expect(screen.getByText('Edit Product')).toBeInTheDocument()
    expect(screen.getByDisplayValue('Test Product')).toBeInTheDocument()
    expect(screen.getByDisplayValue('TEST-001')).toBeInTheDocument()
  })

  it('submits form with valid data', async () => {
    productService.create.mockResolvedValue({ data: { id: 1 } })

    render(
      <ProductForm
        product={null}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    )

    fireEvent.change(screen.getByLabelText(/SKU/i), {
      target: { value: 'NEW-001' }
    })
    fireEvent.change(screen.getByLabelText(/Product Name/i), {
      target: { value: 'New Product' }
    })
    fireEvent.change(screen.getByLabelText(/Price/i), {
      target: { value: '99.99' }
    })
    fireEvent.change(screen.getByLabelText(/Quantity/i), {
      target: { value: '100' }
    })

    fireEvent.click(screen.getByText('Create Product'))

    await waitFor(() => {
      expect(productService.create).toHaveBeenCalled()
      expect(mockOnSubmit).toHaveBeenCalled()
    })
  })

  it('calls onClose when cancel is clicked', () => {
    render(
      <ProductForm
        product={null}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    )

    fireEvent.click(screen.getByText('Cancel'))
    expect(mockOnClose).toHaveBeenCalled()
  })

  it('validates required fields', async () => {
    render(
      <ProductForm
        product={null}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    )

    fireEvent.click(screen.getByText('Create Product'))

    // Form should not submit without required fields
    await waitFor(() => {
      expect(productService.create).not.toHaveBeenCalled()
    })
  })
})
