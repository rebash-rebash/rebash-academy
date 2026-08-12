---
title: "Free Subnet Calculator | CIDR Calculator | IP Address Calculator"
description: "Free online Subnet Calculator. Calculate Network Address, Broadcast Address, CIDR, Wildcard Mask, Host Range, Binary Conversion, IPv4 Class, and more instantly."
author: Shaik Basha
last_updated: "2026-08-12"
category: tools
tags:
  - tools
  - subnet-calculator
  - cidr
  - ipv4
  - networking
  - wildcard-mask
comments: false
hide:
  - toc
---

# Subnet Calculator

<div id="ra-tool-subnet" class="ra-tool" data-ra-tool="subnet"></div>

<div class="ra-tool-ref" id="ra-tool-ref">
  <div class="ra-tool__tile ra-tool-ref__cheat">
    <h3 class="ra-tool-ref__title">CIDR Cheat Sheet</h3>
    <div class="ra-tool-ref__scroll">
      <table class="ra-tool-cheatsheet">
        <thead>
          <tr>
            <th>CIDR</th>
            <th>Subnet Mask</th>
            <th>Usable Hosts</th>
            <th>Notes</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>/32</td><td>255.255.255.255</td><td>1</td><td>Single host</td></tr>
          <tr><td>/31</td><td>255.255.255.254</td><td>2</td><td>Point-to-point (RFC 3021)</td></tr>
          <tr><td>/30</td><td>255.255.255.252</td><td>2</td><td>Common for WAN / P2P</td></tr>
          <tr><td>/29</td><td>255.255.255.248</td><td>6</td><td></td></tr>
          <tr><td>/28</td><td>255.255.255.240</td><td>14</td><td></td></tr>
          <tr><td>/27</td><td>255.255.255.224</td><td>30</td><td></td></tr>
          <tr><td>/26</td><td>255.255.255.192</td><td>62</td><td></td></tr>
          <tr><td>/25</td><td>255.255.255.128</td><td>126</td><td></td></tr>
          <tr><td>/24</td><td>255.255.255.0</td><td>254</td><td>Common LAN</td></tr>
        </tbody>
      </table>
    </div>
    <p class="ra-tool-ref__more">
      <a href="#ra-cidr-full" data-ra-full-table>View full table →</a>
    </p>
  </div>

  <div class="ra-tool__tile ra-tool-ref__private">
    <h3 class="ra-tool-ref__title">Common Private Networks</h3>
    <table class="ra-tool-private">
      <tbody>
        <tr data-ra-preset="10.0.0.0/8" tabindex="0" role="button">
          <td class="ra-tool-private__cidr">10.0.0.0/8</td>
          <td class="ra-tool-private__label">Class A Private</td>
        </tr>
        <tr data-ra-preset="172.16.0.0/12" tabindex="0" role="button">
          <td class="ra-tool-private__cidr">172.16.0.0/12</td>
          <td class="ra-tool-private__label">Class B Private</td>
        </tr>
        <tr data-ra-preset="192.168.0.0/16" tabindex="0" role="button">
          <td class="ra-tool-private__cidr">192.168.0.0/16</td>
          <td class="ra-tool-private__label">Class C Private</td>
        </tr>
        <tr data-ra-preset="100.64.0.0/10" tabindex="0" role="button">
          <td class="ra-tool-private__cidr">100.64.0.0/10</td>
          <td class="ra-tool-private__label">CGNAT (ISP Shared)</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<div class="ra-tool__tile ra-tool-ref__full" id="ra-cidr-full" hidden>
  <h3 class="ra-tool-ref__title">Full CIDR table</h3>
  <div class="ra-tool-ref__scroll">
    <table class="ra-tool-cheatsheet">
      <thead>
        <tr>
          <th>CIDR</th>
          <th>Subnet Mask</th>
          <th>Usable Hosts</th>
          <th>Notes</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>/32</td><td>255.255.255.255</td><td>1</td><td>Single host</td></tr>
        <tr><td>/31</td><td>255.255.255.254</td><td>2</td><td>Point-to-point (RFC 3021)</td></tr>
        <tr><td>/30</td><td>255.255.255.252</td><td>2</td><td>Common for WAN / P2P</td></tr>
        <tr><td>/29</td><td>255.255.255.248</td><td>6</td><td></td></tr>
        <tr><td>/28</td><td>255.255.255.240</td><td>14</td><td></td></tr>
        <tr><td>/27</td><td>255.255.255.224</td><td>30</td><td></td></tr>
        <tr><td>/26</td><td>255.255.255.192</td><td>62</td><td></td></tr>
        <tr><td>/25</td><td>255.255.255.128</td><td>126</td><td></td></tr>
        <tr><td>/24</td><td>255.255.255.0</td><td>254</td><td>Common LAN</td></tr>
        <tr><td>/23</td><td>255.255.254.0</td><td>510</td><td></td></tr>
        <tr><td>/22</td><td>255.255.252.0</td><td>1,022</td><td></td></tr>
        <tr><td>/21</td><td>255.255.248.0</td><td>2,046</td><td></td></tr>
        <tr><td>/20</td><td>255.255.240.0</td><td>4,094</td><td></td></tr>
        <tr><td>/19</td><td>255.255.224.0</td><td>8,190</td><td></td></tr>
        <tr><td>/18</td><td>255.255.192.0</td><td>16,382</td><td></td></tr>
        <tr><td>/17</td><td>255.255.128.0</td><td>32,766</td><td></td></tr>
        <tr><td>/16</td><td>255.255.0.0</td><td>65,534</td><td>Class B sized</td></tr>
        <tr><td>/12</td><td>255.240.0.0</td><td>1,048,574</td><td>RFC 1918 Class B block</td></tr>
        <tr><td>/10</td><td>255.192.0.0</td><td>4,194,302</td><td>CGNAT (RFC 6598)</td></tr>
        <tr><td>/8</td><td>255.0.0.0</td><td>16,777,214</td><td>Class A sized</td></tr>
      </tbody>
    </table>
  </div>
</div>
