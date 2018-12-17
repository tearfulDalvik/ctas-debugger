//
//  ViewController.swift
//  CTAS
//
//  Created by 丰丰哥 on 2018/12/16.
//  Copyright © 2018 丰丰哥. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    
    @IBOutlet weak var btn_a: UIButton!
    @IBOutlet weak var btn_b: UIButton!
    @IBOutlet weak var btn_c: UIButton!
    @IBOutlet weak var btn_d: UIButton!
    
    @IBOutlet weak var btn_prev: UIButton!
    @IBOutlet weak var btn_subq: UIButton!
    
    lazy var serverAddr: String = "";
    var isConnected = false;

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
    }
    
    @IBAction func onA(_ sender: Any) {
        let url = URL(string: serverAddr + "answer/a")
        pb_connect.startAnimating()
        self.btn_a.isEnabled = false
        self.btn_b.isEnabled = false
        self.btn_c.isEnabled = false
        self.btn_d.isEnabled = false
        self.btn_prev.isEnabled = false
        self.btn_subq.isEnabled = false
        
        let task = URLSession.shared.dataTask(with: url!) {(data, response, error) in
            guard data != nil else {
                DispatchQueue.main.async {
                    self.tv_state.text = "Can not connect to specified server."
                    self.tv_state.isHidden = false
                    self.pb_connect.stopAnimating()
                    self.btn_connect.isHidden = false
                }
                return
            }
                DispatchQueue.main.async {
                    if let httpResponse = response as? HTTPURLResponse {
                        switch(httpResponse.statusCode) {
                            case 200:
                                self.tv_server.text = "OK!"
                            case 503:
                                self.tv_server.text = "Connected to server but not attached to CTAS System"
                            default:
                                self.tv_server.text = "Faild"
                        }
                    }
                    self.pb_connect.stopAnimating()
                    self.et_ip.isHidden = true
                    self.tv_state.isHidden = true
                    self.isConnected = true
                    self.btn_a.isEnabled = true
                    self.btn_b.isEnabled = true
                    self.btn_c.isEnabled = true
                    self.btn_d.isEnabled = true
                    self.btn_prev.isEnabled = true
                    self.btn_subq.isEnabled = true
                }
        }
        
        task.resume()
    }
    
    @IBOutlet weak var pb_connect: UIActivityIndicatorView!
    @IBOutlet weak var tv_server: UILabel!
    @IBOutlet weak var tv_state: UILabel!
    @IBOutlet weak var btn_connect: UIButton!
    @IBOutlet weak var et_ip: UITextField!
    @IBAction func onConnect(_ sender: Any) {
        pb_connect.startAnimating()
        self.tv_state.isHidden = true
        self.btn_connect.isHidden = true
        let ip = et_ip.text
        serverAddr = "http://" + ip! + ":12346/"
        let url = URL(string: serverAddr + "handshake")
        
        let task = URLSession.shared.dataTask(with: url!) {(data, response, error) in
            guard let data = data else {
                DispatchQueue.main.async {
                    self.tv_state.text = "Can not connect to specified server."
                    self.tv_state.isHidden = false
                    self.pb_connect.stopAnimating()
                    self.btn_connect.isHidden = false
                }
                return
            }
            do {
                let result = try JSONDecoder().decode(APIResult.self, from: data as Data)
                if(result.status != "ok") {
                    throw NSError()
                }
                DispatchQueue.main.async {
                    self.tv_server.text = "Connected to " + self.serverAddr + " (2ms)"
                    self.pb_connect.stopAnimating()
                    self.et_ip.isHidden = true
                    self.tv_state.isHidden = true
                    self.isConnected = true
                    self.btn_a.isEnabled = true
                    self.btn_b.isEnabled = true
                    self.btn_c.isEnabled = true
                    self.btn_d.isEnabled = true
                    self.btn_prev.isEnabled = true
                    self.btn_subq.isEnabled = true
                    self.handleResponse(result: result)
                }
                
            } catch {
                DispatchQueue.main.async {
                    self.tv_state.text = "Can not understand specified server."
                    self.tv_state.isHidden = false
                    self.pb_connect.stopAnimating()
                    self.btn_connect.isHidden = false
                }
            }
        }
        
        task.resume()
    }
    
    func handleResponse(result: APIResult) {
        if(result.message != "") {
            let alert = UIAlertController(title: "Message", message: result.message, preferredStyle: UIAlertController.Style.alert)
            alert.addAction(UIAlertAction(title: "Dismiss", style: UIAlertAction.Style.default, handler: nil))
            self.present(alert, animated: true)
        }
    }
    
    struct APIResult: Decodable {
        let status: String
        let message: String
        let version: Int
        
        enum CodingKeys : String, CodingKey {
            case status = "status"
            case message = "message"
            case version = "version"
        }
    }
}

