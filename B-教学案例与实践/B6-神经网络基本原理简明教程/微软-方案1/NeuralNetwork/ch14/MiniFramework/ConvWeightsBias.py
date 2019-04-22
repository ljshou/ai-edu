# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

#coding=utf-8

import numpy as np

from MiniFramework.WeightsBias import *

"""
Weights and Bias: 一个Weights可以包含多个卷积核Kernal，一个卷积核可以包含多个过滤器Filter
WK - Kernal 卷积核数量(等于输出通道数量), 每个WK有一个Bias
WC - Channel 输入通道数量
FH - Filter Height
FW - Filter Width
"""
class ConvWeightsBias(WeightsBias):
    def __init__(self, output_c, input_c, filter_h, filter_w, init_method, optimizer_name, eta):
        self.KernalCount = output_c
        self.FilterCount = input_c
        self.FilterHeight = filter_h
        self.FilterWidth = filter_w
        self.init_method = init_method
        self.optimizer_name = optimizer_name
        self.eta = eta

        self.initial_value_filename = str.format("_{0}_{1}_{2}_{3}_{4}_init.npy", 
                                                 self.KernalCount, 
                                                 self.FilterCount, 
                                                 self.FilterHeight, 
                                                 self.FilterWidth, 
                                                 self.init_method.name)
        self.result_value_filename = str.format("_{0}_{1}_{2}_{3}_{4}_result.npy", 
                                                 self.KernalCount, 
                                                 self.FilterCount, 
                                                 self.FilterHeight, 
                                                 self.FilterWidth, 
                                                 self.init_method.name)

        self.WeightsShape = (self.KernalCount, self.FilterCount, self.FilterHeight, self.FilterWidth)

    def CreateNew(self):
        self.W = ConvWeightsBias.InitialConvParameters(self.WeightsShape, self.init_method)
        self.B = np.zeros((self.KernalCount, 1))
        self.SaveInitialValue()

    def Rotate180(self):
        self.WT = np.zeros(self.W.shape)
        for i in range(self.KernalCount):
            for j in range(self.FilterCount):
                self.WT[i,j] = np.rot90(self.W[i,j], 2)
        return self.WT

    def ClearGrads(self):
        self.dW = np.zeros(self.W.shape)
        self.dB = np.zeros(self.B.shape)

    def MeanGrads(self, m):
        self.dW = self.dW / m
        self.dB = self.dB / m

    def Update(self):
        self.W = self.W - self.eta * self.dW
        self.B = self.B - self.eta * self.dB

    @staticmethod
    def InitialConvParameters(shape, method):
        
        assert(len(shape) == 4)
        num_input = shape[2]
        num_output = shape[3]
        
        if method == InitialMethod.Zero:
            W = np.zeros(shape)
        elif method == InitialMethod.Normal:
            W = np.random.normal(size=shape)
        elif method == InitialMethod.MSRA:
            W = np.random.normal(0, np.sqrt(2/num_input*num_output), size=shape)
        elif method == InitialMethod.Xavier:
            W = np.random.uniform(-np.sqrt(6/(num_output+num_input)),
                                  np.sqrt(6/(num_output+num_input)),
                                  size=shape)
        return W

