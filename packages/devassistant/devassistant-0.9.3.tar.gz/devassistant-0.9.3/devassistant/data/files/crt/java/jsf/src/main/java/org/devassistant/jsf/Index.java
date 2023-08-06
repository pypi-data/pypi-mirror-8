package org.devassistant.jsf;

import java.io.Serializable;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.ViewScoped;

@ManagedBean
@ViewScoped
public class Index implements Serializable {

	public Index(){
	}

	public String getText(){
		return "This text comes from a backing bean.";
	}
}
